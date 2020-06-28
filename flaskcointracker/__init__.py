from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flaskcointracker.models import User
import sys
import os
#from flaskcointracker.models import db

#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
#db_file = "sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app = Flask(__name__) #intialize flask app
app.config.from_object('config')
#app.config["SQLALCHEMY_DATABASE_URI"] = db_file
#app.config.from_pyfile('config.py') #having this now does't matter, it would just overwrite what i have
db = SQLAlchemy(app)

#db.app = app
#db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

import flaskcointracker.views
from flaskcointracker.models import User




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




if __name__ == "__main__":
    app.run()