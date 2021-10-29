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
from bson.objectid import ObjectId
from time import time
from flask_mail import Message
from application import mailing
import jwt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
        
        return redirect(url_for('users.build_profile', username=session["user"]))
    
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
        
    return render_template('build-profile.html')



@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_username = request.form.get("username").lower()
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


@users.route("/edit-profile/<username>", methods = ["GET", "POST"])
def edit_profile(username):

    user = User.get_user(username)

    if request.method == "POST":
        
        if not username:
            flash("You need to be logged in to edit your profile")
            return redirect("users.login")

        display_spotify_playlists = "on" if request.form.get("display_spotify_playlists") else "off"
        is_artist = "on" if request.form.get("is_artist") else "off"

        edited_info = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "date_of_birth": request.form.get("date_of_birth"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "about_user": request.form.get("about_user"),
            "spotify_userID": request.form.get("spotify_userID"),
            "display_spotify_playlists": display_spotify_playlists,
            "is_artist": is_artist
        }

        user.edit_profile(username, edited_info)
        session["user"] = user.username
        flash("Your profile has been updated")
        return redirect(url_for("users.user_profile", username=session["user"]))



        
               

@users.route("/logout")
def logout():
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('main.index'))



@users.route("/file/<path:filename>")
def display_profile_image(filename):

    try:
        profile_image = mongo.send_file(filename)
        return profile_image
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None
 


@users.route("/user-profile/<username>")
def user_profile(username):
    """
    Invokes function to query MongoDB user collection
    by username in URL parameter. Displays user's details
    collected in build_profile function, as well as 
    user's tracks.
    """
    current_user = User.find_user_by_username(username)

    all_tracks = Track.bind_users_to_tracks()
   
    liked_tracks = []

    if current_user:

    # Iterate over all tracks and iterate over user's liked tracks
    # Check for matching ObjectIDs between 'tracks' collection
    # and 'liked_tracks' array in 'user' document.
        if "liked_tracks" in current_user:
            for track in all_tracks:
                for liked_track in current_user["liked_tracks"]:
                    if liked_track == ObjectId(track["_id"]):
                        liked_tracks.append(track)


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
        print(users_tracks)

    return render_template("user-profile.html", username=current_user,
                             user_age=user_age, users_tracks=users_tracks,
                             liked_tracks=liked_tracks)


# https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968

def get_reset_token(email, expires_sec=500):
    """
    Generates and returns JSON Web Token to be used for authorization
    """

    user = User.find_user_by_email(email)
    user_id = str(user["_id"])

   
    s = Serializer(os.environ.get("SECRET_KEY"), expires_sec)
    return (s.dumps({"user_id": user_id}).decode('utf-8'))

@users.route('/request-password-reset', methods=["GET", "POST"])
def request_password_reset():
    """
    Handles form on modal in login.html
    =========================================
    Checks email input against User collection in MongoDB.
    If successful, creates JSON web token using get_user_token()
    Instance of Flask mail is created with properties:

    Subject
    Sender - Environment variable
    Recipients - The email provided by the user
    HTML - 'password-reset-email.html'
           Called from render_template(). 
           Takes in JWT and user's first name as argument

    Email is then sent with a link provided to visit
    'reset-password.html', with the token included in
    GET request.
    """
    
    if request.method == "POST":

        email_input = request.form.get("email_address")

        # Query MongoDB to check user input against email address in DB
        user = User.find_user_by_email(email_input)
        if not user:
            flash("We're sorry, we couldn't find your email.")
            return redirect("users.login")

        token = get_reset_token(email_input)

        msg = Message()
        msg.subject = "Cross//Tracks: Reset your Password"
        msg.sender = os.environ.get("MAIL_USERNAME")
        msg.recipients = [user["email_address"]]
        msg.html = render_template('password-reset-email.html', 
                                    token=token, 
                                    user=user["first_name"].title())
        mailing.send(msg)
        

    return render_template('login.html')

def verify_reset_token(token):
    """
    Decodes the JSON web token
    and return's user email address 
    if successful. If unsuccessful,
    (primarily due to the token timing out),
    Flash message is displayed with relevant
    error message and User is redirected to login 
    page.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    s = Serializer(SECRET_KEY)
    
    try:
        user_id = s.loads(token)["user_id"]
    except Exception as e:
        print(e)
        return None
    
    found_user = User.find_user_by_id(user_id)
    return found_user
    

@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    user = verify_reset_token(token)
    

    # if request.method == "POST":

    #     password = request.form.get("password")
    #     confirm_password = request.form.get("confirm_password")

    #     if not User.validate_password_format(password):
    #         flash("Please include at least one capital letter and one number")
    #         return redirect(url_for("users.reset_password"))

    #     if not User.validate_password_match(password, confirm_password):
    #         flash("Passwords do not match!")
    #         return redirect(url_for("users.reset_password"))

        



    
    return render_template('reset-password.html')











        
   
