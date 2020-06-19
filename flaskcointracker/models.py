#from flaskcointracker import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flaskcointracker import db
from flaskcointracker import bcrypt

#db = SQLAlchemy()

class User(UserMixin, db.Model):
    #__tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(128))
    #sites = db.relationship('Site', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        self._password = bcrypt.generate_password_hash(value)


    def __repr__(self):
            return '<User %r>' % self.email