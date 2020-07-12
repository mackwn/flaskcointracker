import os

#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir,"cointracker.db"))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_file
SECRET_KEY = 'WLfwPp90oVKW-Q3q72MkcA'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
BCRYPT_LOG_ROUNDS = 12
