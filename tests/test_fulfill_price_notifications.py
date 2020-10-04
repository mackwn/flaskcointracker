import os
import tempfile
import pytest
import flaskcointracker
from flaskcointracker.models import Notification
from flaskcointracker.helpers import check_notifications
import datetime

def test_notifications_unfulfilled_by_default(client):
    assert len(Notification.query.filter(Notification.fulfilled_date == None).all()) == 4

def test_fulfill_notification(client):
    prices = {
        'btc-usd-coinbase':{'price':3000,'date':datetime.datetime.utcnow()},
        'eth-usd-coinbase':{'price':300,'date':datetime.datetime.utcnow()}
    }
    check_notifications(prices)
    assert len(Notification.query.filter(Notification.fulfilled_date == None).all()) == 0


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
            user = User(email="testuser3@test.com",password="testpass")
            flaskcointracker.db.session.add(user)
            flaskcointracker.db.session.commit()
            # Bullish notification BTC
            note = Notification(price=2000,initial_price=1000, coin='btc-usd-coinbase',owner=user)
            # Bullish notification Eth
            note2 = Notification(price=250,initial_price=100, coin='eth-usd-coinbase',owner=user)
            # Bearish notification BTC
            note3 = Notification(price=4000,initial_price=5000, coin='btc-usd-coinbase',owner=user)
            # Bearish notification Eth
            note4 = Notification(price=400,initial_price=500, coin='eth-usd-coinbase',owner=user)
            flaskcointracker.db.session.add(note)
            flaskcointracker.db.session.add(note2)
            flaskcointracker.db.session.add(note3)
            flaskcointracker.db.session.add(note4)
            flaskcointracker.db.session.commit()
            #user = User.query.first()
            #print(user.notifications.first())
            #print(len(user.notifications.all()))

        yield client
    flaskcointracker.db.session.remove()
    flaskcointracker.db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)