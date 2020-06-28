from flask_wtf import FlaskForm as Form #I love Tina
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
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
