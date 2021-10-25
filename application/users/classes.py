"""
User Class
==============

Handles all user data that will be created, read, 
updated and deleted to MongoDB, as well as password
validation.

"""

from application import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import re


class User():
    """
    Class represents the User instance

    Attributes:
    ==============
        _id (ObjectId): the user's id (provided by MongoDB)

        username (str): the user's chosen username to be stored in session

        email (str): the user's email address

        first_name (str): the user's first name

        last_name (str): the user's last name

        date_of_birth (date): the user's date of birth, used to determine age

        city (str): an optional field for user to provide their city of residence

        country (str): an optional field for user to provide their country of residence

        about_user (str): an optional field for user to provide brief description

        profile_image (binData): an optional field for user's profile image

        is_artist (bool): optional field for user to display their artist status

    
    Methods:
    =============
        get_info():
            Prepares user information ready for MongoDB handling.

        register():
            Inputs user information into MongoDB

        login():
            Logs user into session (subject to validation)

        logout():
            Logs user out of session

        find_user_by_id(): 
            Finds an individual user by their ObjectId

        find_all_users():
            Queries MongoDB for a list of all users

        validate_password_match():
            Verifies that 'Confirm Password' matches first password
            upon registering.

        validate_password_format():
            Verifies that the password meets specified format criteria

        edit_profile():
            Updates MongoDB with updates fields provided by user

        change_password():
            Updates MongoDB with new password, in the case user forgets
            original password.

        change_email():
            Updates MongoDB with user's new email address.

        delete_user():
            Deletes user from database
     """

    def __init__(self, username, password, email_address=None,
                first_name=None, last_name=None, date_of_birth=None,
                city=None, country=None, about_user=None, 
                profile_image=None, is_artist=None, spotify_userID=None,
                display_spotify_playlists=None, _id=None, liked_tracks=None):

        """
        Initialise user instance
        """

        self.username = username
        self.password = generate_password_hash(password)
        self.email_address = email_address if isinstance(email_address, str) else str("")
        self.first_name = first_name if isinstance(first_name, str) else str("")
        self.last_name = last_name if isinstance(last_name, str) else str("")
        self.date_of_birth = date_of_birth if isinstance(date_of_birth, str) else str("")
        self.city = city if isinstance(city, str) else str("")
        self.country = country if isinstance(country, str) else str("")
        self.about_user = about_user if isinstance (about_user, str) else str("")
        self.profile_image = profile_image if isinstance(profile_image, str) else str('')
        self.is_artist = is_artist if isinstance(is_artist, bool) else False
        self.spotify_userID = spotify_userID if isinstance(spotify_userID, str) else str("")
        self.display_spotify_playlists = display_spotify_playlists if isinstance(
            display_spotify_playlists, bool) else False
        self.id = _id
        self.liked_tracks = liked_tracks if isinstance(liked_tracks, list) else []
        

    
    
    def get_user_info(self):
        """
        Collects and prepares user input in
        register and profile build functions.
        """

        user_info = {
            "username": self.username,
            "password": self.password,
            "email_address": self.email_address.lower(),
            "first_name": self.first_name.lower(),
            "last_name": self.last_name.lower(),
            "date_of_birth": self.date_of_birth,
            "city": self.city,
            "country": self.country,
            "about_user": self.about_user,
            "profile_image": self.profile_image,
            "is_artist": self.is_artist,
            "spotify_userID": self.spotify_userID,
            "display_spotify_playlists": self.display_spotify_playlists
            
        }

        return user_info

    def prepare_liked_track(self):

        liked_track_info = {
            "liked_tracks": self.liked_tracks
        }
        
        return liked_track_info


    def add_liked_track(self, track_id):

        self.liked_tracks.append(ObjectId(track_id))
        # print("liked tracks:", self.liked_tracks)

        mongo.db.users.update_one({
            "_id": ObjectId(self.id),
        }, {
            "$set": self.prepare_liked_track()
        })

    
    def remove_liked_track(self, track_id):

        if ObjectId(track_id) in self.liked_tracks:
            self.liked_tracks.remove(ObjectId(track_id))
            mongo.db.users.update_one({
                "_id": ObjectId(self.id),
            }, {
                "$set": self.prepare_liked_track()
            })



    @classmethod
    def get_user(cls, username):
        """
        Queries MongoDB to locate a user by their ID
        Utilised in users/views.py in functions:

        edit_profile
        """

        user_data = mongo.db.users.find_one({"username": username})

        if user_data is not None:
            return cls(**user_data)
        else:
            user_data = None
            return False


    @staticmethod
    def get_all_users():

        return mongo.db.users.find()

    
    @staticmethod
    def get_id(username):
        
        user_id = mongo.db.users.find_one({"username":username})["_id"]

        return user_id


    @staticmethod
    def complete_user_profile(username, profile_info):

        
        mongo.db.users.update_one({"username": username}, {"$set": profile_info})


    @staticmethod
    def find_user_by_username(username):
        """
        Queries MongoDB for username
        Utilised in users/views.py in register 
        function, to determine if username
        already exists.
        """
        return mongo.db.users.find_one({"username": username})

    def register(self):
        """
        Invokes get_user_info() and inserts data
        into MongoDB
        """

        user_data = self.get_user_info()

        mongo.db.users.insert_one(user_data)


    @staticmethod
    def validate_password_match(password, confirm_password):

        return password == confirm_password
        
        
    @staticmethod
    def validate_password_format(password):

        pattern = "^[a-zA-Z0-9]{8,15}$"
        return re.search(pattern, password)

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])
        return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def check_image_filesize(filesize):
        max_img_filesize = 0.5 * 1024 * 1024

        if int(filesize) <= max_img_filesize:
            return True
        else:
            return False

    @staticmethod
    def add_profile_image(username, profile_image):

        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.update_one({"username": username},
                                  {"$set": profile_image})

    
    @staticmethod
    def return_profile_image(filename):

        return mongo.send_file(filename)


    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


    
