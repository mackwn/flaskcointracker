from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
#from flask_sqlalchemy import SQLAlchemy
#from flaskcointracker.models import User
import sys
import os
from flaskcointracker.models import db
from flaskcointracker.models import User


project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
db_file = "sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app = Flask(__name__) #intialize flask app
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db.app = app
db.init_app(app)
            
#Routes
@app.route('/')
def homepage():
    return render_template("main.html")



if __name__ == "__main__":
    app.run()