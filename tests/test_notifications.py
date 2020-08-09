import os
import tempfile
import pytest
import flaskcointracker
from flaskcointracker.models import Notification

# Helpers
def userlogin(email,password,client):
    client.post('/login',data={
        'email':"{email}".format(email=email),
        'password':"{password}".format(password=password)
    }, follow_redirects=True)
    User = flaskcointracker.models.User
    user = User.query.filter_by(email=email).first()
    return user


def test_create_notification(client):
    # if not logged on
    ## no link on homepage 
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login or create an account' in response.data
    ## path not allowed for non logged on users
    response = client.get('notifications/new')
    assert response.status_code == 302
    # logged on user can create notifications
    user = userlogin('testuser@test.com','testpass',client)
    assert user
    ## link on homepage
    response = client.get('/')
    assert response.status_code == 200
    assert b'New Price Notification' in response.data
    ## the correct template is served
    response = client.get('notifications/new')
    assert response.status_code == 200
    for phrase in ['Coin','Target Price']:
        assert bytes('{phrase}'.format(phrase=phrase),encoding='utf8') in response.data
    
    #init_count = len(user.notifications.all())
    #init_count = len(Notification.query.all())
    ## creating the notification works
    response = client.post('/notifications/new',data={
        'coin':'btc-usd-coinbase',
        'price':300
    }, follow_redirects=True)
    assert response.status_code == 200
    #assert len(user.notifications.all()) == init_count+1
    assert len(Notification.query.filter_by(user_id=1).all()) == 2

def test_delete_notifications(client):
    # User must be logged on
    response = client.post('notifications/1/delete')
    assert response.status_code == 302
    # Can only delete your own notifications
    user = userlogin('testuser@test.com','testpass',client)
    response = client.post('notifications/2/delete')
    assert response.status_code == 404
    # Can't delete notification that doesn't exist'
    response = client.post('notifications/4/delete')
    assert response.status_code == 404
    # Actually works
    ## get request
    response = client.get('notifications/1/delete')
    assert response.status_code == 200
    assert b'Are you sure you want to delete this notification?' in response.data
    ## post
    response = client.post('notifications/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert len(Notification.query.filter_by(user_id=1).all()) == 0



def test_notifications_index(client):
    pass 


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
            note = Notification(price=250,coin='btc-usd-coinbase',owner=User.query.first())
            note2 = Notification(price=250,coin='btc-usd-coinbase',owner=user2)
            flaskcointracker.db.session.add(note)
            flaskcointracker.db.session.add(note2)
            flaskcointracker.db.session.commit()
            user = User.query.first()
            print(user.notifications.first())
            print(len(user.notifications.all()))

        yield client
    flaskcointracker.db.session.remove()
    flaskcointracker.db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)