import requests
import datetime as dt

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

    return prices

if __name__ == "__main__":
    prices = coinbase_spot_prices()
    print(prices)