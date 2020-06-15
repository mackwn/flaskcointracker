import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

from src.models import db
from src.models.user import User

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir,"cointracker.db"))

app = Flask(__name__) #intialize flask app
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db.app = app
db.init_app(app)