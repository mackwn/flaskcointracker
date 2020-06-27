#
from flaskcointracker import app, db, bcrypt
from flask import render_template, redirect, request, current_app, session, \
    flash, url_for, abort
from flaskcointracker import forms
from flaskcointracker.models import User
# Static Pages
@app.route('/')
def homepage():
    return render_template("main.html")

# Views for User
## Authenticate User
@app.route('/login', methods=["GET","POST"])
def login():
    form = forms.EmailPasswordLoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        users = User.query.all()

        if not user or not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect username or password.')
            return redirect(url_for('login'))

        return redirect(url_for('homepage'))

    return render_template("login.html", form=form)


## Create User
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



## View User
@app.route('/users/<user_id>') 
def view_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: return abort(404)
    return render_template('user.html', user=user)


## Edit User

## Delete User

## Login User

## Logout User



# NOTIFICATION








