"""
User Class
==============

Handles all user data that will be created, read, 
updated and deleted to MongoDB, as well as password
validation.

"""

from datetime import _date
from application import mongo
from bson.objectid import ObjectId
from werkzeug import generate_password_hash

class User:
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

    def __init__(self, _id, username, email_address, password,
                first_name=None, last_name=None, date_of_birth=None,
                city=None, country=None, about_user=None, 
                profile_image=None, is_artist=None, spotify_userID=None,):

        """
        Initialise user instance
        """
    
        self.id = _id
        self.username = username
        self.email = email_address
        self.password = generate_password_hash(password)
        self.first_name = first_name if isinstance(first_name, str) else str("")
        self.last_name = last_name if isinstance(last_name, str) else str("")
        self.date_of_birth = date_of_birth if isinstance(date_of_birth, str) else str("")
        self.city = city if isinstance(city, str) else str("")
        self.country = country if isinstance(country, str) else str("")
        self.profile_image = profile_image if isinstance(profile_image, bytes) else None
        self.is_artist = is_artist if isinstance(is_artist, bool) else False
        self.spotify_userID = spotify_userID if isinstance(spotify_userID, str) else str("")

    
    
    def get_user_info(self):

        user_info = {
            "username": self.username,
            "password": self.password,
            "email_address": self.email_address.lower(),
            "first_name": self.first_name.lower(),
            "last_name": self.last_name.lower(),
            "date_of_birth": self.date_of_birth,
            "city": self.city,
            "country": self.country,
            "profile_image": self.profile_image,
            "is_artist": self.is_artist,
            "spotify_userID": self.spotify_userID
        }

        return user_info

    def register(self):
        """
        Invokes get_user_info() and inserts data
        into MongoDB
        """

        user_data = self.get_user_info()

        mongo.db.insert_one(user_data)

    

    
