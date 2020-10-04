#
from flaskcointracker import app, db, bcrypt
from flask import render_template, redirect, request, current_app, session, \
    flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from flaskcointracker import forms
from flaskcointracker.models import User, Notification, Coin
import requests
from flaskcointracker.helpers import coinbase_spot_prices, coin_dict

# Static Pages
@app.route('/')
def homepage():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
    else: user = None
    prices = coinbase_spot_prices()
    return render_template("main.html",prices=prices, coin_dict=coin_dict, user=user)

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

    #print(form.errors)
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
    # validate that the requested user exists
    if not user: return abort(404)
    #  validate that users are requesting themselves 
    if current_user.id != user.id: 
        print('accessing user that isnt logged on')
        return redirect(url_for('view_user',user_id = int(current_user.id)))
    # load notifications
    notifications = user.notifications.all()

    return render_template('user.html', user=user, notifications=notifications)

# User Index
@app.route('/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('user_index.html', users=users)

## Update User
@app.route('/users/<user_id>/update', methods=["GET","POST"])
@login_required
def update_user(user_id):
    if int(user_id) != int(current_user.id):  
        print(user_id)
        print(current_user.id)
        print(user_id == current_user.id)
        return abort(404)
    user = User.query.filter_by(id=int(user_id)).first()
    form = forms.EmailPasswordUpdateForm()
    form.email.default = user.email
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(user.password, form.old_password.data):
            flash('Incorrect password.')
            return redirect(url_for('update_user',user_id = int(current_user.id)))

        # change email only
        if (form.email.data != user.email) and (len(form.password.data) == 0):
            user.email = form.email.data
            db.session.commit()
        # change password only
        if (form.email.data == user.email) and (len(form.password.data) > 0):
            user.password = form.password.data
            db.session.commit()
        # change both
        if (form.email.data != user.email) and (len(form.password.data) > 0):
            user.email = form.email.data
            user.password = form.password.data
            db.session.commit()
        return redirect(url_for('view_user',user_id = int(current_user.id)))

    return render_template("user_update.html", form=form,user=user)

## Delete User
@app.route('/users/<user_id>/delete', methods=["GET","POST"])
@login_required
def delete_user(user_id):
    if int(user_id) != int(current_user.id):  
        return abort(404)
    user = User.query.filter_by(id=int(user_id)).first()
    form = forms.PasswordDeleteForm()

    if form.validate_on_submit():
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Incorrect password.')
            return redirect(url_for('delete_user',user_id = int(current_user.id)))
        logout_user()
        #User.query.filter_by(id=int(user_id)).first().delete()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('homepage'))
        
    return render_template('delete_user.html',form=form)




# NOTIFICATION
# index
@app.route('/notifications')
@login_required
def view_notifications():
    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/notifications/new',methods=['GET','POST'])
@login_required
def create_notification():
    user = User.query.get(current_user.id)
    form = forms.NotificationForm()
    # current_price = 400
    if form.validate_on_submit():
        print('validating form')
        saved_coin = Coin.query.filter(Coin.name==form.coin.data).first()
        print(saved_coin)
        print(saved_coin is None)
        if saved_coin is not None:
            current_price = saved_coin.price 
            print(saved_coin.price)
            print(saved_coin.name)
        else:
            flash('Unable to create notification. Please try again.')
            #return redirect(url_for('create_notification'))
            print('yo not a coin')

            return abort(404)

        note = Notification(
            price = form.price.data,
            coin = form.coin.data,
            initial_price = current_price,
            owner = user
        )
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('view_user',user_id = int(current_user.id)))

    return render_template('create_notification.html', form=form)


@app.route('/notifications/<notification_id>/delete',methods=['GET','POST'])
@login_required
def delete_notification(notification_id):
    note = Notification.query.get(notification_id)
    if not note: return abort(404)
    if note.user_id != current_user.id:
        return abort(404)
    form = forms.NotificationDeleteForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(url_for('view_user',user_id = int(current_user.id)))

    return render_template('delete_notification.html', form=form)

    







