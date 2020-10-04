import os
import tempfile
import pytest
import flaskcointracker
from flaskcointracker.models import Coin
from flaskcointracker.helpers import update_coin_prices
import datetime

# Helpers
def userlogin(email,password,client):
    client.post('/login',data={
        'email':"{email}".format(email=email),
        'password':"{password}".format(password=password)
    }, follow_redirects=True)
    User = flaskcointracker.models.User
    user = User.query.filter_by(email=email).first()
    return user

def test_update_coin_prices(client):

    spot_prices = {
        'btc-usd-coinbase':{'price':100,'date':datetime.datetime.utcnow()},
        'eth-usd-coinbase':{'price':50,'date':datetime.datetime.utcnow()}
    }
    update_coin_prices(spot_prices)
    assert Coin.query.filter(Coin.name=='btc-usd-coinbase').first().price == 100
    assert Coin.query.filter(Coin.name=='eth-usd-coinbase').first().price == 50






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
            Coin = flaskcointracker.models.Coin
            coin = Coin(price=0,name='btc-usd-coinbase', exchange='coinbase')
            coin2 = Coin(price=0,name='eth-usd-coinbase', exchange='coinbase')
            flaskcointracker.db.session.add(coin)
            flaskcointracker.db.session.add(coin2)
            flaskcointracker.db.session.commit()

        yield client
    flaskcointracker.db.session.remove()
    flaskcointracker.db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)