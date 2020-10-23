from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from celery import Celery
from celery.task.base import periodic_task
from datetime import timedelta
from flask_mail import Mail
#from flaskcointracker.models import User
import sys
import os
#from flaskcointracker.models import db


#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
#db_file = "sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

# APP
app = Flask(__name__) #intialize flask app
app.config.from_object('config')

# CELERY
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#app.config["SQLALCHEMY_DATABASE_URI"] = db_file
#app.config.from_pyfile('config.py') #having this now does't matter, it would just overwrite what i have
# ORM
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.app = app
#db.init_app(app)

# ENCRYPTION
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# EMAIL
mail = Mail(app)

from flaskcointracker.models import User, Notification
from flaskcointracker.helpers import coinbase_spot_prices, check_notifications, update_coin_prices
import flaskcointracker.views
from flaskcointracker.emails import price_notification_emails

app.logger.info('Server up')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@periodic_task(run_every=timedelta(seconds=30))
def periodic_run_get_prices():
    spot_prices = coinbase_spot_prices()
    check_notifications(spot_prices)
    new_notifications = update_coin_prices(spot_prices)
    if len(new_notifications) > 0:
        price_notification_emails(new_notifications)

    return


if __name__ == "__main__":
    app.run()