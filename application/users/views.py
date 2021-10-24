"""
User Views
==========

Sub-module to handle routes and data input relative
to user details.
"""

import os

from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request,
                   session)
from application.users.classes import User
from application.tracks.classes import Track
from application import Config
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from application.helpers.users import calculate_user_age
from application import mongo
if os.path.exists("env.py"):
    import env




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
        
        return redirect(url_for('users.build_profile', username=username))
    
    return render_template('register.html')





@users.route("/profile-edit/<username>", methods=["GET", "POST"])
def build_profile(username):
    """
    build_profile() runs after initial registration, to gather information
    to be displayed on user's profile page.
    """

    if request.method == "POST":

        if 'profile_image' in request.files:

            allowed_filesize = User.check_image_filesize(request.cookies.get('filesize'))
            if not allowed_filesize:
                flash('Your file is too large!')
                return redirect(url_for("users.build_profile", username=session["user"]))

            profile_image = request.files['profile_image']
            if profile_image:

                if profile_image.filename == '':
                    flash("Your image must have a filename!")
                    return redirect(url_for('users.build_profile', username=session["user"]))

                allowed_image = User.allowed_file(profile_image.filename)

                if not allowed_image:
                    flash("Images can have extensions 'jpg', 'jpeg', 'gif', 'png' and 'pdf' only.")
                    return redirect(url_for('users.build_profile', username=username))

                else:
                    mongo.save_file(profile_image.filename, profile_image)
                
                
            profile_info = {
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "date_of_birth": request.form.get("date_of_birth"),
                "city": request.form.get("city"),
                "country": request.form.get("country"),
                "about_user": request.form.get("about_user"),
                "spotify_userID": request.form.get("spotify_userID"),
                "display_spotify_playlists": request.form.get("display_spotify_playlists"),
                "is_artist": request.form.get("is_artist"),
                "profile_image": profile_image.filename
                }

            User.complete_user_profile(username, profile_info)

            return redirect(url_for("users.user_profile", username = username))
        
    return render_template('profile-edit.html')



@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_username = request.form.get("username")
        login_password = request.form.get("password")

        user = User.find_user_by_username(login_username.lower())
        if user:
            password_check = User.check_password(
                             user["password"],
                             login_password)
            if password_check:
                session["user"] = login_username
                flash("Welcome back {}".format(login_username))
                return redirect(url_for("users.user_profile", username=session["user"]))
            
            else:
                flash("Invalid username/password")
                return redirect(url_for("users.login"))
        else:
            flash("Invalid username/password")
            return redirect(url_for("users.login"))

        
    return render_template("login.html")       
        
               
@users.route("/logout")
def logout():
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('main.index'))


@users.route("/file/<path:filename>")
def display_profile_image(filename):
    print(filename)
    return mongo.send_file(filename)


@users.route("/user-profile/<username>")
def user_profile(username):
    """
    Invokes function to query MongoDB user collection
    by username in URL parameter. Displays user's details
    collected in build_profile function, as well as 
    user's tracks.
    """
    current_user = User.find_user_by_username(username)

    user_dob = current_user["date_of_birth"]
    user_age = None
    
    # Converts D.O.B string into tuple, preparing for calculate_user_age
    if user_dob:
        user_dob = tuple(map(int, user_dob.split('-')))
        user_age = calculate_user_age(user_dob)

    user_profile_image = current_user["profile_image"]

    # Display user's tracks
    user_id = User.get_id(username)

    if user_id is not None:

        users_tracks = Track.get_users_tracks(user_id)

    return render_template("user-profile.html", username=current_user,
                             user_age=user_age, users_tracks=users_tracks)

        
   
