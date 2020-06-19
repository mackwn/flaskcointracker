#
from flaskcointracker import app, db
from flask import render_template, redirect, request, current_app, session, \
    flash, url_for
from flaskcointracker import forms
from flaskcointracker.models import User
# Static Pages
@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/login', methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route('/sign-up', methods=["GET","POST"])
def register():
    form = forms.EmailPasswordForm()
    print('is the form valid?')
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        print('yup, form is valid')
        user = User(email=form.email.data, password=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template("create_user.html", form=form)

# USER

## Create User

## Users

## View User

## Edit User

## Delete User

## Login User

## Logout User



# NOTIFICATION








