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
#from flaskcointracker.models import User
import sys
import os
#from flaskcointracker.models import db


#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
#db_file = "sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app = Flask(__name__) #intialize flask app
app.config.from_object('config')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#app.config["SQLALCHEMY_DATABASE_URI"] = db_file
#app.config.from_pyfile('config.py') #having this now does't matter, it would just overwrite what i have
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.app = app
#db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


from flaskcointracker.models import User, Notification
from flaskcointracker.helpers import coinbase_spot_prices, check_notifications
import flaskcointracker.views

app.logger.info('Server up')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@periodic_task(run_every=timedelta(seconds=30))
def periodic_run_get_prices():
    coinbase_spot_prices()
    return


if __name__ == "__main__":
    app.run()