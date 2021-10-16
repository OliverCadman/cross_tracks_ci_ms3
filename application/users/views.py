"""
User Views
==========

Sub-module to handle routes and data input relative
to user details.
"""

from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request,
                   session)
from application.users.classes import User

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register_user():

    if request.method == "POST":

        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email_address = request.form.get("email_address")

        if not User.validate_password_match(password,
                                            confirm_password):
            flash("Passwords do not match")
            return render_template("index.html")

        if not User.validate_password_format(password):
            flash("Password format invalid")
            return render_template("index.html")

        
        
        if User.find_user_by_username(username):
            flash("Username already exists")
            return redirect(url_for("main.index"))

        

        new_user = User(username, password, email_address)

        new_user.register()
        flash("Registration Successful")
        session["user"] = request.form.get("username").lower()
        return redirect(url_for('users.build_profile'))
    
    return render_template('register.html')



@users.route("/profile-edit")
def build_profile():
    return render_template('profile-edit.html')


@users.route("/logout")
def logout():

    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('main.index'))
    
   

