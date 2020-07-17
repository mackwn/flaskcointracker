#from flaskcointracker import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flaskcointracker import db
from flaskcointracker import bcrypt
import datetime

#db = SQLAlchemy()

class User(UserMixin, db.Model):
    #__tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    notifications = db.relationship('Notification', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        self._password = bcrypt.generate_password_hash(value)


    def __repr__(self):
            return '<User %r>' % self.email

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(30))
    price = db.Column(db.Float)
    initial_price = db.Column(db.Float)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    fulfilled_date = db.Column(db.DateTime)
    fulfilled_price = db.Column(db.Float)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
            return '<Notification %r>' % self.id