import requests
import datetime as dt
from collections import OrderedDict 
from flaskcointracker import db
from flaskcointracker.models import Notification, Coin
import datetime

coin_dict = OrderedDict({
    'btc-usd-coinbase':['Bitcoin'],
    'eth-usd-coinbase':['Ethereum']
})

def update_coin_prices(spot_prices):
    '''
    This iterates over the dictionary spotprices, checks to see if there's any  
    Coin with the same name as spotprice, if it does - update the price.
    '''
    for coin_name in spot_prices.keys():
        saved_coin = Coin.query.filter(Coin.name==coin_name).first()
        if saved_coin is not None:
            saved_coin.price = spot_prices[coin_name]
            try:
                db.session.commit()
            except:
                print('Unable to update price for {}'.format(coin_name))


def coinbase_spot_prices():
    ''' Get spotprices for cryptocurrencies by their api. Return prices for all the coins 
    in a dictionary with name and price '''
    def _coinbase_spot(currency_pair):
        response = requests.get(
        'https://api.coinbase.com/v2/prices/{currency_pair}/spot'.format(currency_pair=currency_pair),
        )
        price = float(response.json()['data']['amount'])
        date = dt.datetime.strptime(response.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
        return  {'price':price,'date':date}
    pairs = {'btc-usd-coinbase':'BTC-USD','eth-usd-coinbase':'ETH-USD'}
    
    prices = {}
    for k, v in pairs.items():
        prices[k] = _coinbase_spot(v)

    #app.logger.info('Bitcoin price: {}'.format(prices['Bitcoin']['price']))
    #app.logger.info('Ethereum price: {}'.format(prices['Ethereum']['price']))
    print('Bitcoin price: {}'.format(prices['btc-usd-coinbase']['price']))
    print('Ethereum price: {}'.format(prices['eth-usd-coinbase']['price']))

    return prices

def check_notifications(prices, coin_dict=coin_dict):

    for coin_name in coin_dict.keys():
        # current price should come from calling coin model otherwise, work the same.
        # this could by improved by having a many to one relationship of coins to notifications
        # coindict still serves a purpose as a way to control which coins get notifications.
        # this could be improved later by adding a display name column to coin

        curr_price = prices[coin_name]

        notes = Notification.query.filter(
            (Notification.coin == coin_name) &
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