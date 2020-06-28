#
from flaskcointracker import app, db, bcrypt
from flask import render_template, redirect, request, current_app, session, \
    flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
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
        remember = request.form.get('remember')
        user = User.query.filter_by(email=email).first()


        if not user or not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect username or password.')
            return redirect(url_for('login'))

        login_user(user,remember=remember)
        return redirect(url_for('homepage'))

    return render_template("login.html", form=form)

## Logout User
@app.route('/logout')
@login_required
def logout():
    print('about to log out')
    logout_user()
    print('user logged out')
    return redirect(url_for('homepage'))

## Create User
@app.route('/sign-up', methods=["GET","POST"])
def register():
    form = forms.EmailPasswordForm()
    # print('is the form valid?')
    # if form.is_submitted():
    #     print("submitted")

    # if form.validate():
    #     print("valid")

    print(form.errors)
    if form.validate_on_submit():
        #print('yup, form is valid')
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('homepage'))
    return render_template("create_user.html", form=form)



## View User
@app.route('/users/<user_id>') 
@login_required
def view_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: return abort(404)
    if current_user.id != user.id: 
        print('accessing user that isnt logged on')
        return redirect(url_for('view_user',user_id = int(current_user.id)))
    return render_template('user.html', user=user)


## Edit User

## Delete User

## Login User

## Logout User



# NOTIFICATION








