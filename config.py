import os
from dotenv import load_dotenv

load_dotenv()
#project_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir,"cointracker.db"))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = db_file
else: SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Celery
if os.environ.get('REDIS_URL') is None:
    redis_url = 'redis://127.0.0.1:6379/0'
else: redis_url = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = redis_url
CELERY_RESULT_BACKEND = redis_url
BCRYPT_LOG_ROUNDS = 12

# Email
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'apikey'
MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

# SETTINGS
NOREPLY = os.environ.get('NOREPLY')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
MAX_NOTIFICATIONS=5
MAX_USERS=15

