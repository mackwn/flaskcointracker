from flask_mail import Message
from flask import render_template, current_app
from threading import Thread
from flaskcointracker import app, mail
from flaskcointracker.helpers import coin_dict
#from flaskcointracker.models import Notification


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    #app = current_app._get_current_object()
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def price_notification_emails(notes):

    for note in notes:
        #note = Notification.query.get(note_id)
        subject = 'Cointracker - {coin} is now {price}'.format(
            coin=coin_dict[note.coin],
            price=note.fulfilled_price
        )

        send_email(subject,
                [note.owner.email],
                # ideal to use render template
                # render template needs to be inside app.app_conext()
                # render template causes a detached record error that I can't seem to resolve
                # These should be the only emails needed for this demo level app (in any
                # event, other emails like password reset will be handeled in views and shouldn't
                # have this issue)

                # render_template("notification_email.txt", 
                #                 note=note, coindict=coindict, user_email=user_email),
                # render_template("notification_email.html", 
                #                 note=note, coindict=coindict, user_email=user_email))

                text_notification_template(note, coin_dict),
                html_notification_template(note, coin_dict)
            )

def html_notification_template(note, coindict):
    return '''
        <p>{email},</p>

        <p>Your notification for {coin_name} has been fulfilled.</p> 

        <ul>
            <li>Current price: {fulfilled_price} at {fulfilled_date}</li> 
            <li>Target price: {price}.</li>
            <li> Original price: {initial_price} at {created} </li> 
        </ul>

        <p>Flaskcointracker</p>
        '''.format(
                email=note.owner.email, coin_name=coindict[note.coin], 
                fulfilled_price=note.fulfilled_price,
                fulfilled_date=note.fulfilled_date, price=note.price , 
                initial_price=note.initial_price, created=note.created
            )

def text_notification_template(note, coindict):
    return '''
        {email},

        Your notification for {coin_name} has been fulfilled. 
        Current price: {fulfilled_price} at {fulfilled_date}. 
        Target price: {price}. Original price: {initial_price} at 
        {created}. 

        Flaskcointracker
        '''.format(
                email=note.owner.email, coin_name=coindict[note.coin], 
                fulfilled_price=note.fulfilled_price,
                fulfilled_date=note.fulfilled_date, price=note.price , 
                initial_price=note.initial_price, created=note.created
            )

