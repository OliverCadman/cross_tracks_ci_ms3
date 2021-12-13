"""
Main: Sub-module

Handles views for Home Page and Contact Page

Handles data from form input in Contact Page
and sends email to website owner.

Views:
    index()

    contact()

Functions:
    send_email()
"""


from flask import render_template, url_for, Blueprint, request, flash, redirect
from application import mailing
from flask_mail import Message
import os

# Initialize 'main' blueprint
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
def index():
    """
    Renders the website's home page.
    """
    return render_template("index.html")


@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Renders the website's contact page.
    """
    return render_template("contact.html")


@main.route("/send_email", methods=["GET", "POST"])
def send_email():
    """
    Handles data submitted from form in
    Contact page. Flask Mail utilised
    to send email to website owner, in
    html format ("contact-message.html")
    """
    if request.method == "POST":

        sender = request.form.get("full_name")
        sender_email = request.form.get("email_address")
        message = request.form.get("questions_comments")

        msg = Message()
        msg.subject = "Cross//Tracks Feedback/Query"
        msg.sender = sender_email
        msg.recipients = ['o.cadman@live.co.uk']
        msg.html = render_template('contact-message.html',
                                   user='Oliver', sender_name=sender,
                                   sender_email=sender_email, message=message)

        try:
            mailing.send(msg)
            flash("Thanks for contacting us! We will reply shortly")
            return redirect(url_for('main.contact'))
        except:
            flash('Sorry, something went wrong. Please try again')
            return redirect(url_for('main.contact'))
