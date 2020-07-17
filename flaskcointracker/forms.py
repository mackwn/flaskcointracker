from flask_wtf import FlaskForm as Form #I love Tina
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flaskcointracker.helpers import coin_dict

class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

class PasswordDeleteForm(Form):
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

class EmailPasswordLoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EmailPasswordUpdateForm(Form):
    email = StringField('Email', validators=[Email()])
    old_password = PasswordField('Existing Password', validators=[DataRequired()])
    password = PasswordField('Password', [
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')

class NotificationForm(Form):
    price = DecimalField('Price',places=2,validators=DataRequired())
    coin = SelectField('Coin', choices=[(k, v[0]) for k, v in coin_dict.items()],
        validators=[DataRequired()])

class NotificationDeleteForm(Form):
    submit = SubmitField('Delete')