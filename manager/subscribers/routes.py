from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message

from manager import db, mail, app
from manager.model import Subscribers
from manager.subscribers.utils import email_validator

from threading import Thread

subs_bp = Blueprint('subs', __name__)


def send_async_mail(application, msg):
    """
    Message for invoking mail.send under an application context.
    Takes a flask application and the message as parameters

    Parameters
    ----------
    application
        A flask application
    msg
        A flask mail Message instance

    """
    with application.app_context():
        mail.send(msg)


def send_email():
    """
    Function to send mail to all the users with subject, text body, html body, article url and published date.
    Rendered in an email template. A threaded function to send the email to multiple users in shortened time.

    """
    published_date = str(datetime.now().date())
    with app.app_context():
        recipients = [user.email for user in Subscribers.query.all() if user.is_active]
        article_url = 'https://me.me/i/none-can-do-me-a-bamboozle-not-one-heck-~mrs-doge-5531225'
        msg = Message('Campaign', sender='noreply@fincdemo.com', recipients=recipients)
        msg.body = 'Lorem ipsum blah blah blah'
        msg.html = render_template('email_template.html', published_date=published_date, article_url=article_url)
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()


@subs_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Post request for user subscription. Accepts email and first_name through request arguments.
    Validates email as well.

    Returns
    -------
    json : json
        json object of a dictionary with message

    """
    try:
        request_data = request.json
        user = Subscribers.query.filter_by(email=request_data['email']).first()
        if not email_validator(request_data['email']):
            return jsonify({
                'message': 'invalid email'
            })
        if user is None:
            new_user = Subscribers(email=request_data['email'],
                                   first_name=request_data['first_name'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                'message': 'user subscribed successfully'
            })
        elif user is not None and not user.is_active:
            user.subscribe()
            db.session.commit()
            return jsonify({
                'message': 'user subscribed successfully'
            })
        return jsonify({
            'message': 'user already subscribed'
        })
    except TypeError:
        return jsonify({
            'message': 'email or first_name not provided'
        })
    except KeyError:
        return jsonify({
            'message': 'email or first_name not provided'
        })


@subs_bp.route('/unsubscribe')
def unsubscribe():
    """
    GET request for un-subscribing from email notifications. Inactivates the user.

    Returns
    -------
    json : json
        json object of a dictionary with message

    """
    try:
        subscriber = Subscribers.query.filter_by(email=request.args['email']).first()
        if subscriber is not None:
            subscriber.unsubscribe()
            db.session.commit()
            return jsonify({
                'message': 'user successfully unsubscribed'
            })
        else:
            return jsonify({
                'message': 'no such user exist'
            })
    except TypeError:
        return jsonify({
            'message': 'email or first_name not provided'
        })
    except KeyError:
        return jsonify({
            'message': 'email or first_name not provided'
        })
