# https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
from flask.cli import FlaskGroup

from flaskcointracker import app, db
from flaskcointracker.models import Coin

cli = FlaskGroup(app)


@cli.command("seed_db")
def seed_db():
    btc = Coin(name='btc-usd-coinbase', exchange='coinbase', price=0)
    eth = Coin(name='eth-usd-coinbase', exchange='coinbase', price=0)
    db.session.add(btc)
    db.session.add(eth)
    db.session.commit()

if __name__ == "__main__":
    cli()