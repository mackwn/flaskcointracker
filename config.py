import os

#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir,"cointracker.db"))

SQLALCHEMY_DATABASE_URI = db_file
SECRET_KEY = 'WLfwPp90oVKW-Q3q72MkcA'
BCRYPT_LOG_ROUNDS = 12
