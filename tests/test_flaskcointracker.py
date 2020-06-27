import os
import tempfile
import pytest
import flaskcointracker

# Model Tests
#def test_user():
    #User = flaskcointracker.models.User


# Integration Tests

def test_homepage(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Home page yo - Salvete omnes' in response.data

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
    assert b'Home page yo - Salvete omnes' in response.data
    added_user = flaskcointracker.models.User.query.filter(
        flaskcointracker.models.User.email == TESTEMAIL
    ).first()
    ## new user added to the database
    assert added_user
    new_user_count = flaskcointracker.models.User.query.count()
    ## new user count increased 
    assert new_user_count == user_count+1

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
    assert b'Home page yo - Salvete omnes' in response.data

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
    User = flaskcointracker.models.User
    user = User.query.filter_by(id=1).first()
    response = client.get('users/1')
    assert response.status_code == 200
    assert bytes('{email}'.format(email=user.email),encoding='utf8') in response.data
    response = client.get('users/100')
    assert response.status_code == 404

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
            flaskcointracker.db.session.commit()
        yield client

    os.close(db_fd)
    os.unlink(db_file)