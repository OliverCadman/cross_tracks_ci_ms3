"""
User: Sub-module
==========

Sub-module to handle routes and data relating
to users.

Views:
    build_profile()

    login()

    user_profile()


Functions:

    register_user()

    edit_profile()

    logout()

    display_profile_image()

    edit_profile_img()

    get_reset_token()

    request_password_reset()

    verify_reset_token()

    reset_password()

    delete_profile()
"""

import os

from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request,
                   session, abort)
from application.users.classes import User
from application.tracks.classes import Track
from application.comments.classes import Comment
from application import Config
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from application.helpers.users import calculate_user_age
from application import mongo
from bson.objectid import ObjectId
from time import time
from flask_mail import Message
from application import mailing
from urllib.parse import urlparse

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
if os.path.exists("env.py"):
    import env


# Initialize users blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register_user():
    """
    Renders "register.html" template

    Handles data submitted through form in
    Register page

    Checks if the submitted username already
    exists in the database.

    Uses password validation to ensure the
    password is in the correct format, and
    that the first password matches the
    confirmed password.

    If all checks are passed, a new User
    object is instantiated and registered,
    and a session cookie is created, assigned
    to the username provided in registration
    form.
    """

    if request.method == "POST":

        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email_address = request.form.get("email_address")

        if not User.validate_password_match(password,
                                            confirm_password):
            flash("Passwords do not match")
            return redirect(request.referrer)

        if not User.validate_password_format(password):
            flash("Password format invalid")
            return redirect(request.referrer)

        if User.find_user_by_username(username):
            flash("Username already exists")
            return redirect(request.referrer)

        new_user = User(username, password, email_address)

        new_user.register()
        flash("Registration Successful")
        session["user"] = request.form.get("username").lower()

        return redirect(url_for('users.build_profile',
                                username=session["user"]))

    return render_template('register.html')


@users.route("/profile-edit/<username>", methods=["GET", "POST"])
def build_profile(username):
    """
    Renders "build-profile.html"

    Runs after initial registration, and handles form
    data submitted in Build Profile page.

    If the user selects a profile image, methods in
    User class are used to validate file format and
    size. If all checks are passed, the file is saved
    to mongodb fs.files and fs.chunks collections.

    Dictionary is made containing data submitted through
    form, and passed into User class' static method
    "complete_user_profile()"
    """

    if request.method == "POST":

        if 'profile_image' in request.files:

            profile_image = request.files['profile_image']

            if profile_image.filename != '':

                allowed_filesize = User.check_image_filesize(
                                        request.cookies.get('filesize'))
                if not allowed_filesize:
                    flash('Your file is too large!')
                    return redirect(url_for("users.build_profile",
                                            username=session["user"]))

                allowed_image = User.allowed_file(profile_image.filename)

                if not allowed_image:
                    flash(("Images can have extensions 'jpg'",
                           "'jpeg', 'gif', 'png' and 'pdf' only."))
                    return redirect(url_for('users.build_profile',
                                    username=username))

                else:
                    mongo.save_file(profile_image.filename, profile_image)

            profile_info = {
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "date_of_birth": request.form.get("date_of_birth"),
                "city": request.form.get("city"),
                "country": request.form.get("country"),
                "about_user": request.form.get("about_user"),
                "is_artist": request.form.get("is_artist"),
                "profile_image": profile_image.filename
                }

            User.complete_user_profile(username, profile_info)

            return redirect(url_for("users.user_profile",
                                    username=username))

    return render_template('build-profile.html')


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders "login.html"

    Handles data submitted from login form.

    Finds username in "users" collection.

    Checks that the password matches the
    password hash held in the user document
    in "users" collection.

    If all checks are passed, session cookie
    is created and assigned to username, and
    user is redirected to the home page, with
    welcome message.
    """

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

                flash("Welcome back, {}".format(login_username))
                return redirect(url_for('main.index'))

            else:
                flash("Invalid username/password")
                return redirect(request.referrer)
        else:
            flash("Invalid username/password")
            return redirect(request.referrer)

    # Flash message to give feedback to user if they
    # attempt to like a track without logging in.
    parsed_url = urlparse(request.referrer)

    if parsed_url.path == '/browse-tracks':
        flash('Please login to like tracks!')
    return render_template("login.html")


@users.route("/edit-profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    """
    Handles data submitted from form in modal,
    in User Profile page.

    Organises submitted data into dictionary,
    and passed into User class' "edit_profile()"
    method, to updated relative user document in
    mongoDB "users" collection.
    """

    if request.method == "POST":

        if not username:
            flash("You need to be logged in to edit your profile")
            return redirect("users.login")

        is_artist = "on" if request.form.get("is_artist") else "off"

        edited_info = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "date_of_birth": request.form.get("date_of_birth"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "about_user": request.form.get("about_user"),
            "is_artist": is_artist
        }

        try:
            User.edit_profile(username, edited_info)
            flash("Your profile has been updated")
            return redirect(url_for("users.user_profile",
                                    username=session["user"]))
        except:
            flash("Sorry, something went wrong. Please try again.")
            return redirect(url_for("users.user_profile",
                                    username=session["user"]))


@users.route("/logout")
def logout():
    """
    Removes "user" session cookie, and
    logs user out, redirecting to website's
    home page.
    """
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for('main.index'))


@users.route("/file/<path:filename>")
def display_profile_image(filename):
    """
    Queries mongoDB fs.files collection using
    filename to match file, and sends profile image
    to client, which is returned to be displayed
    in User Profile page, and on Track cards/modals
    in Browse Tracks page.
    """

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

    # Customize error handling in case of invalid URL path
    if User.find_user_by_username(username) is None:
        abort(404)

    current_user = User.find_user_by_username(username)

    all_tracks = Track.bind_users_to_tracks()

    # Acquire genres to display in edit track modal
    genres = Track.get_genres()

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

    # Display user's tracks
    user_id = User.get_id(username)

    if user_id is not None:

        users_tracks = Track.get_users_tracks(user_id)

    return render_template("user-profile.html", username=current_user,
                           user_age=user_age, users_tracks=users_tracks,
                           liked_tracks=liked_tracks, genres=genres)


@users.route('/edit_profile_img/<username>', methods=["GET", "POST"])
def edit_profile_img(username):
    """
    Handles image file uploaded from User Profile
    page.

    Finds existing profile image data in fs.files
    and fs.chunks collections, and removes them, ready
    to be replaced with new image data.

    If successful, the new image data is saved to
    mongoDB, and filename is updated to user collection.
    """

    if request.method == "POST":

        user = User.find_user_by_username(username)

        if user is not None:

            profile_image = request.files["profile_image"]
            print(profile_image)
            if profile_image.filename != '':

                existing_file = User.find_file_by_filename(
                                user['profile_image'])

                if existing_file is not None:

                    filename_id = existing_file["_id"]

                    try:
                        User.delete_profileimage_file(filename_id)

                    except Exception as e:

                        flash("Sorry, something went wrong. Please try again")
                        return redirect(url_for('users.user_profile',
                                                username=username))

                updated_info = {
                    "profile_image": profile_image.filename
                }

                try:
                    User.update_profile_image(username, profile_image.filename,
                                              profile_image, updated_info)

                    flash('Profile image successfully updated')
                    return redirect(url_for('users.user_profile',
                                            username=username))
                except Exception as e:
                    flash('Sorry, something went wrong. Please try again.')
                    return redirect(url_for('users.user_profile',
                                            username=username))


# https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968
def get_reset_token(email, expires_sec=500):
    """
    Generates and returns JSON Web Token to be used for authorization
    """

    user = User.find_user_by_email(email)
    user_id = str(user["_id"])

    SECRET_KEY = "/G..;U7|cf1>^B&"

    s = Serializer('SECRET_KEY', expires_sec)
    token = s.dumps({"user_id": user_id}).decode('utf-8')
    return token


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

    SECRET_KEY = "/G..;U7|cf1>^B&"

    s = Serializer('SECRET_KEY')
    user_id = None

    try:
        user_id = s.loads(token)["user_id"]
    except Exception as e:
        print(e)
        return None

    found_user = User.find_user_by_id(user_id)
    return found_user


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Renders "reset-password.html"

    Handles data submitted in form in Reset Password
    page.

    Checks that the password matches the correct format,
    and the first password matches the confirmed password.

    If all checks are passed, the new password is updated in
    user collection, and user is redirected to home page.
    """

    # Grabs user ID returned from verify_reset_token()
    user = verify_reset_token(token)
    print(user)

    # if request.method == "POST":

    #     password = request.form.get("password")
    #     confirm_password = request.form.get("confirm_password")

    #     if not User.validate_password_format(password):
    #         flash(("Please include at least one",
    #               " capital letter and one number"))
    #         return render_template('reset-password.html')

    #     if not User.validate_password_match(password, confirm_password):
    #         flash("Passwords do not match!")
    #         return render_template('reset-password.html')

    #     username = user["username"]
    #     edited_password = {
    #         "password": generate_password_hash(password)
    #     }

    #     User.edit_profile(username, edited_password)
    #     flash("Password changed successfully!")
    #     return redirect("main.index")

    return render_template('reset-password.html')


@users.route('/delete_profile/<username>')
def delete_profile(username):
    """
    Deletes user's account from "users" collection

    Removes all tracks attributed to user from
    "tracks" collection, as well as all attributed
    tracks listed in user's "liked_tracks" arrays.

    Username is removed from "track" collection's
    "likes" list, wherever the username matches.

    All comments that the user submitted are also
    removed.

    User profile image data is removed from fs.files
    and fs.chunks collections.

    User is then popped out of the session cookie,
    and returned to the home page with flash message.
    """

    if not session["user"]:
        return redirect(url_for("users.login"))

    current_user = User.find_user_by_username(username)

    if current_user:

        user_id = current_user["_id"]

        user_profile_image = current_user["profile_image"]
        if user_profile_image != '':
            profile_filename = User.find_file_by_filename(
                user_profile_image)
            print(profile_filename)

            filename_id = profile_filename["_id"]

            if filename_id:
                try:
                    # Remove image data from fs.files and fs.chunks
                    User.delete_profileimage_file(filename_id)
                except Exception as e:
                    print(e)

        try:
            # Remove user document from "users" collection
            User.delete_user(user_id)
        except Exception as e:
            print(e)

        try:
            # Remove user data from track's "likes" list
            # and decrement the 'likes' count of all
            # relative tracks.
            Track.decrement_likes_count(username)
            Track.remove_user_from_likes_list(username)
        except Exception as e:
            print(e)

        try:
            # Remove all comments linked to user_id
            Comment.delete_comments_by_user_id(user_id)
        except Exception as e:
            print(e)

        session.pop("user")
        flash('Your account has been deleted')
        return redirect(url_for("main.index"))

    return redirect(url_for("users.user_profile", username=username))
