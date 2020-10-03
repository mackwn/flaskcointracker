import requests
import datetime as dt
from collections import OrderedDict 
from flaskcointracker import db
from flaskcointracker.models import Notification
import datetime

coin_dict = OrderedDict({
    'btc-usd-coinbase':['Bitcoin'],
    'eth-usd-coinbase':['Ethereum']
})

def coinbase_spot_prices():
    def _coinbase_spot(currency_pair):
        response = requests.get(
        'https://api.coinbase.com/v2/prices/{currency_pair}/spot'.format(currency_pair=currency_pair),
        )
        price = float(response.json()['data']['amount'])
        date = dt.datetime.strptime(response.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
        return  {'price':price,'date':date}
    pairs = {'Bitcoin':'BTC-USD','Ethereum':'ETH-USD'}
    
    prices = {}
    for k, v in pairs.items():
        prices[k] = _coinbase_spot(v)

    #app.logger.info('Bitcoin price: {}'.format(prices['Bitcoin']['price']))
    #app.logger.info('Ethereum price: {}'.format(prices['Ethereum']['price']))
    print('Bitcoin price: {}'.format(prices['Bitcoin']['price']))
    print('Ethereum price: {}'.format(prices['Ethereum']['price']))

    return prices

def check_notifications(prices, coin_dict=coin_dict):
    for coin, coin_name in coin_dict.items():
        curr_price = prices[coin_name[0]]

        notes = Notification.query.filter(
            (Notification.coin == coin) &
            (
                (
                    (Notification.price > Notification.initial_price) & 
                    (Notification.price < curr_price['price'])
                ) |
                (
                    (Notification.price < Notification.initial_price) & 
                    (Notification.price > curr_price['price'])
                )
            )
        ).all()

        # Would be nice to see if there's a better way to do this than without another for look
        for note in notes:
            # update each with initial price
            note.fulfilled_price = curr_price['price']
            note.fulfilled_date = curr_price['date']
            db.session.commit()

if __name__ == "__main__":
    prices = coinbase_spot_prices()
    print(prices)