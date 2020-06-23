from flask_wtf import Form #I love Tina
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')