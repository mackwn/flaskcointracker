import os

#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir,"cointracker.db"))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_file
SECRET_KEY = os.environ.get('SECRET_KEY')
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
BCRYPT_LOG_ROUNDS = 12

# email server
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'apikey'
MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

# SETTINGS
NOREPLY = os.environ.get('NOREPLY')
MAX_NOTIFICATIONS=5

