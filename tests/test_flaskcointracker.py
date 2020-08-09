import os
import tempfile
import pytest
import flaskcointracker

homepage_text = b'Flask Coin Tracker - Current Spot Prices'

# Model Tests
#def test_user():
    #User = flaskcointracker.models.User
# Helpers
def userlogin(email,password,client):
    client.post('/login',data={
        'email':"{email}".format(email=email),
        'password':"{password}".format(password=password)
    }, follow_redirects=True)
    User = flaskcointracker.models.User
    user = User.query.filter_by(email=email).first()
    return user


# Integration Tests

def test_homepage(client):
    response = client.get('/')

    assert response.status_code == 200
    assert homepage_text in response.data

def test_signup(client):

    # Get login page loads
    response = client.get('/sign-up')
    assert response.status_code == 200
    for phrase in ['Email Address','Password','Confirm Password']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data

    # Sign up a user
    user_count = flaskcointracker.models.User.query.count()
    TESTEMAIL = 'test3@test.com'
    TESTPASSWORD = '123badpassword'
    ## add a new user with a valid 
    response = client.post('/sign-up',data={
        'email':TESTEMAIL,
        'password':TESTPASSWORD,
        'confirm':TESTPASSWORD
    },follow_redirects=True)
    assert response.status_code == 200
    ## redirected to homepage 
    assert homepage_text in response.data
    added_user = flaskcointracker.models.User.query.filter(
        flaskcointracker.models.User.email == TESTEMAIL
    ).first()
    ## new user added to the database
    assert added_user
    new_user_count = flaskcointracker.models.User.query.count()
    ## new user count increased 
    assert new_user_count == user_count+1
    ## added user password hashed correctly
    assert flaskcointracker.bcrypt.check_password_hash(added_user.password,TESTPASSWORD) 

    ## can't create user with unconfirmed password
    TESTEMAIL2 = 'testest@test.com'
    response = client.post('/sign-up',data={
        'email':TESTEMAIL2,
        'password':TESTPASSWORD,
        'confirm':'notpassword'
    },follow_redirects=True)

    assert b'Passwords must match' in response.data

    added_user = flaskcointracker.models.User.query.filter(
        flaskcointracker.models.User.email == TESTEMAIL2
    ).first()
    assert not added_user

    ## need valid email format
    notemail = 'clearnotanemail'
    response = client.post('/sign-up',data={
        'email':notemail,
        'password':TESTPASSWORD,
        'confirm':TESTPASSWORD
    },follow_redirects=True)

    assert b'Invalid email address' in response.data
    #with client.session_tr

    added_user = flaskcointracker.models.User.query.filter(
        flaskcointracker.models.User.email == notemail
    ).first()
    assert not added_user
    
def test_login(client):
    # test get
    response = client.get('/login')
    assert response.status_code == 200

    # test login with good credentials
    response = client.post('/login',data={
        'email':"testuser@test.com",
        'password':"testpass"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert homepage_text in response.data

    # test login with bad password
    response = client.post('/login',data={
        'email':"testuser@test.com",
        'password':"testpasswrong"
    }, follow_redirects=True)
    assert response.status_code == 200
    for phrase in ['Email','Password','Remember me']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data

    # test login with bad username
    response = client.post('/login',data={
        'email':"testuser@test.com2",
        'password':"testpass"
    }, follow_redirects=True)
    assert response.status_code == 200
    for phrase in ['Email','Password','Remember me']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data

def test_view_user(client):
    # can't access user if not logged on
    response = client.get('users/1')
    assert response.status_code == 302
    # logged in user can see their own profile
    user = userlogin('testuser@test.com','testpass',client)
    response = client.get('users/{}'.format(int(user.id)))
    assert response.status_code == 200
    assert bytes('{email}'.format(email=user.email),encoding='utf8') in response.data
    # non existent users throw a 404
    response = client.get('users/100')
    assert response.status_code == 404
    # accessing a user that isn't you redirects you to your own account
    response = client.get('users/2', follow_redirects=True)
    assert response.status_code == 200
    assert bytes('{email}'.format(email=user.email),encoding='utf8') in response.data
    
def test_logout(client):
    user = userlogin('testuser@test.com','testpass',client)
    response = client.get('logout',follow_redirects=True)
    assert response.status_code == 200
    assert homepage_text in response.data
    response = client.get('users/{}'.format(int(user.id)),follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    
def test_update_user(client):
    # log in required
    response = client.get('users/1/update')
    assert response.status_code == 302

    user = userlogin('testuser@test.com','testpass',client)
    # get update page
    response = client.get('users/{id}/update'.format(id=user.id))
    assert response.status_code == 200
    for phrase in ['Email Address','Password','Confirm New Password']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data

    # user can't post for another user
    response = client.post('users/2/update', data={
        'email':'badactor'
    })
    assert response.status_code == 404
    ## redirects to update page
    new_email = 'new@email.com'
    new_pass = 'newpass'
    # update email only

    oldemail = user.email
    response = client.post('users/{id}/update'.format(id=user.id), data={
        'old_password':'testpass',
        'email':new_email,
        'password':''
    }, follow_redirects=True)
    assert response.status_code == 200
    assert flaskcointracker.models.User.query.get(user.id).email == new_email
    assert oldemail != flaskcointracker.models.User.query.get(user.id).email

    # update password only
    user = flaskcointracker.models.User.query.get(user.id)
    response = client.post('users/{id}/update'.format(id=user.id), data={
        'email':new_email,
        'old_password':'testpass',
        'password':new_pass,
        'confirm':new_pass
    }, follow_redirects=True)
    assert response.status_code == 200
    assert userlogin(new_email ,new_pass ,client)

    # update email and password
    user = flaskcointracker.models.User.query.get(user.id)
    newer_email = 'newer@new.com'
    newer_pass = 'newerpass'
    response = client.post('users/{id}/update'.format(id=user.id), data={
        'email':newer_email,
        'old_password':new_pass,
        'password':newer_pass,
        'confirm':newer_pass
    }, follow_redirects=True)
    assert response.status_code == 200
    #assert flaskcointracker.models.User.query.get(user.id).email == newer_email
    assert userlogin(newer_email, newer_pass, client)

def test_delete_user(client):
    
    # log in required
    response = client.get('users/1/delete')
    assert response.status_code == 302

    user = userlogin('testuser@test.com','testpass',client)
    assert user
    # get update page
    response = client.get('users/{id}/delete'.format(id=user.id))
    assert response.status_code == 200
    for phrase in ['Password','Confirm Password']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data

    # user can't post for another user
    response = client.post('users/2/delete', data={
        'password':'badactor',
        'confirm':'badactor'
    })
    assert response.status_code == 404
    

    old_id = user.id
    response = client.post('users/{id}/delete'.format(id=user.id), data={
        'password':'testpass',
        'confirm':'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert not flaskcointracker.models.User.query.get(old_id)



#Fixtures

@pytest.fixture
def client():
    # temporary db path and db file and rewrite cointracker db config
    db_fd, db_file = tempfile.mkstemp(suffix='.db')
    flaskcointracker.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{db_file}".format(db_file=db_file)
    # set testing config to true, overwriting config default
    flaskcointracker.app.config['TESTING'] = True
    flaskcointracker.app.config['WTF_CSRF_ENABLED'] = False
    flaskcointracker.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #flaskcointracker.app.config['SQLALCHEMY_DATABASE_URI'] = db_fd

    with flaskcointracker.app.test_client() as client:
        with flaskcointracker.app.app_context():
            #db_fd.create_all()
            #db = SQLalchemy(flaskcointracker.app)
            flaskcointracker.db.create_all()
            User = flaskcointracker.models.User
            user = User(email="testuser@test.com",password="testpass")
            flaskcointracker.db.session.add(user)
            user2 = User(email="testuser2@test.com",password="testpass")
            flaskcointracker.db.session.add(user2)
            flaskcointracker.db.session.commit()
        yield client
    flaskcointracker.db.session.remove()
    flaskcointracker.db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)