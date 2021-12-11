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
import jwt
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

    
    Instance Methods:

        get_user_info(self):
            Collects and prepares User object attributes
            and returns dictionary, to be used by register
            method to insert data into mongoDB "users" collection.

        register(self):
            Invokes get_user_info() and inserts returned
            dictionary into mongoDB "users" collection


        prepare_liked_track(self):
            Used in conjunction with class method
            "get_user()", when user likes a track.
            Prepares ID of liked track into a dictionary
            format, and returning the value ready to be
            inserted into mongoDB "users" collection.


        add_liked_track(self, track_id):
            Utilises User object created
            from class method "get_user()". Appends
            ID of liked track to user object's 
            "liked_tracks" array, then updates 
            mongoDB "user" collection with value returned
            from "prepare_liked_track()" instance method.

        remove_liked_track(self, track_id):
            Utilises User object created from class method
            "get_user()". Removes ID of un-liked track from
            user object's "liked_tracks" array, then updates 
            mongoDB "user" collection with value returned
            from "prepare_liked_track()" instance method.

    
    Class Methods:

        get_user(cls, username):
            Queries mongoDB "users" collection,
            and returns a User object ready to be
            accessed by the object's instance methods,
            particularly:

        add_liked_track():
            Utilises User object created
            from class method "get_user()". Appends
            ID of liked track to user object's 
            "liked_tracks" array, then updates 
            mongoDB "user" collection with value returned
            from "prepare_liked_track()" instance method.
            
        remove_liked_track():
            Utilises User object created from class method
            "get_user()". Removes ID of un-liked track from
            user object's "liked_tracks" array, then updates 
            mongoDB "user" collection with value returned
            from "prepare_liked_track()" instance method.


    Static Methods:

        edit_profile():
            Queries mongoDB "users" collection, finding
            a document by username, and updating it with
            edited profile information.

        complete_user_profile():
            Queries mongoDB "users" collection by 
            matching username, and updates document with
            data gathered in "build-profile.html"

        pull_from_list():
            Method used to remove the IDs of liked tracks that
            are attributed to a particular user, who has deleted
            their account, along with all associated tracks that
            they added.

        get_all_users():
            Queries mongoDB "users" collection and returns
            all users.

        get_id():
            Queries mongoDB "users" collection by
            matching username, and returns ID of user.

        find_user_by_id():
            Queries mongoDB "users" collection by
            matching ID, and returns user document.
            Used to find user when JWT token is 
            submitted upon resetting password.


        find_user_by_username(username):
            Queries MongoDB for username
            Utilised in users/views.py in register 
            function, to determine if username
            already exists.


        validate_password_match(password, confirm_password):
            Returns equality between both passwords, to confirm
            that passwords match when a user logs in.

        validate_password_format(password):
            Returns a regex search on the password passed as argument,
            to confirm that a user's password contains at least
            8 characters, one number, one uppercase character,
            and a special character. 


        check_password(password_hash, password):
            Returns werkzeug.security check_password_hash,
            to ensure that the password submitted matches 
            the encrypted password in mongoDB.


        delete_user(user_id):
            Queries mongoDB "users" collection by matching ID,
            and removes user document from the collection.


        allowed_file(filename):
            Used when user selects a profile image.
            Ensures that the user isn't able to upload any
            file format other than an image.

        check_image_filesize(filesize):
            Ensures than an image's filesize can
            be no greater than 500KB.

        update_profile_image(username, filename, 
                             profile_image, updated_info):
            Queries mongoDB "users" collection by matching
            username. And updates profile_image field with
            new profile image filename.

            Saves binary data to mongoDB fs.files and
            fs.chunks collections.

        find_file_by_filename(filename):
            Queries mongoDB "fs.files" collection by matching filename,
            and returns the filename found.

        delete_profileimage_file(_id):
            Queries mongoDB "fs.files" and "fs.chunks" collections,
            and deletes the found filename and binary data.
     """

    def __init__(self, username, password=None, email_address=None,
                first_name=None, last_name=None, date_of_birth=None,
                city=None, country=None, about_user=None, profile_image=None,
                 is_artist=None, _id=None, liked_tracks=None):

        """
        Constructor to create attributes, attributable to User object.
        """

        self.username = username
        self.password = generate_password_hash(password) if isinstance(password, str) else str("")
        self.email_address = email_address if isinstance(email_address, str) else str("")
        self.first_name = first_name if isinstance(first_name, str) else str("")
        self.last_name = last_name if isinstance(last_name, str) else str("")
        self.date_of_birth = date_of_birth if isinstance(date_of_birth, str) else str("")
        self.city = city if isinstance(city, str) else str("")
        self.country = country if isinstance(country, str) else str("")
        self.about_user = about_user if isinstance (about_user, str) else str("")
        self.profile_image = profile_image if isinstance(profile_image, str) else str('')
        self.is_artist = is_artist if isinstance(is_artist, bool) else False
        self.id = _id
        self.liked_tracks = liked_tracks if isinstance(liked_tracks, list) else []
        

    def get_user_info(self):
        """
        Collects and prepares User object attributes
        and returns dictionary, to be used by register
        method to insert data into mongoDB "users" collection.
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
            "display_spotify_playlists": self.display_spotify_playlists,
            "liked_tracks": self.liked_tracks
            
        }

        return user_info


    def register(self):
        """
        Invokes get_user_info() and inserts returned
        dictionary into mongoDB "users" collection
        """

        user_data = self.get_user_info()

        mongo.db.users.insert_one(user_data)    


    def prepare_liked_track(self):
        """
        Used in conjunction with class method
        "get_user()", when user likes a track.
        Prepares ID of liked track into a dictionary
        format, and returning the value ready to be
        inserted into mongoDB "users" collection.
        """

        liked_track_info = {
            "liked_tracks": self.liked_tracks
        }
        
        return liked_track_info


    def add_liked_track(self, track_id):
        """
        Utilises User object created
        from class method "get_user()". Appends
        ID of liked track to user object's 
        "liked_tracks" array, then updates 
        mongoDB "user" collection with value returned
        from "prepare_liked_track()" instance method.
        """

        self.liked_tracks.append(ObjectId(track_id))

        mongo.db.users.update_one({
            "_id": ObjectId(self.id),
        }, {
            "$set": self.prepare_liked_track()
        })

    
    def remove_liked_track(self, track_id):
        """
        Utilises User object created from class method
        "get_user()". Removes ID of un-liked track from
        user object's "liked_tracks" array, then updates 
        mongoDB "user" collection with value returned
        from "prepare_liked_track()" instance method.
        """

        if ObjectId(track_id) in self.liked_tracks:
            self.liked_tracks.remove(ObjectId(track_id))
            mongo.db.users.update_one({
                "_id": ObjectId(self.id),
            }, {
                "$set": self.prepare_liked_track()
            })


    @staticmethod
    def pull_from_list(array, id):
        """
        Method used to remove the IDs of liked tracks that
        are attributed to a particular user, who has deleted
        their account, along with all associated tracks that
        they added.
        """
        
        mongo.db.users.update_many({array: ObjectId(id)},{"$pull": {array: ObjectId(id)}})


    @staticmethod
    def edit_profile(username, edited_info):
        """
        Queries mongoDB "users" collection, finding
        a document by username, and updating it with
        edited profile information.
        """
        
        mongo.db.users.update_one({"username": username},{"$set": edited_info })

    

    @classmethod
    def get_user(cls, username):
        """
        Queries mongoDB "users" collection,
        and returns a User object ready to be
        accessed by the object's instance methods,
        particularly:

        add_liked_track()

        remove_liked_track()
        """

        user_data = mongo.db.users.find_one({"username": username.lower()})

        if user_data is not None:
            return cls(**user_data)
        else:
            user_data = None
            return False


    @staticmethod
    def get_all_users():
        """
        Queries mongoDB "users" collection and returns
        all users.
        """

        return mongo.db.users.find()

    
    @staticmethod
    def get_id(username):
        """
        Queries mongoDB "users" collection by
        matching username, and returns ID of user.
        """
        
        user_id = mongo.db.users.find_one({"username":username})["_id"]

        return user_id


    @staticmethod
    def complete_user_profile(username, profile_info):
        """
        Queries mongoDB "users" collection by 
        matching username, and updates document with
        data gathered in "build-profile.html"
        """

        
        mongo.db.users.update_one({"username": username}, {"$set": profile_info})

    @staticmethod
    def find_user_by_email(email_address):
        """
        Queries mongoDB "users" collection by
        matching email address, and returns
        user document. Used when user requests
        to reset password, and have an email sent 
        to them to reset psasword. 
        """

        return mongo.db.users.find_one({"email_address": email_address})

    @staticmethod
    def find_user_by_id(id):
        """
        Queries mongoDB "users" collection by
        matching ID, and returns user document.
        Used to find user when JWT token is 
        submitted upon resetting password.
        """

        return mongo.db.users.find_one({"_id": ObjectId(id)})


    @staticmethod
    def find_user_by_username(username):
        """
        Queries MongoDB for username
        Utilised in users/views.py in register 
        function, to determine if username
        already exists.
        """
        return mongo.db.users.find_one({"username": username})


    @staticmethod
    def validate_password_match(password, confirm_password):
        """
        Returns equality between both passwords, to confirm
        that passwords match when a user logs in.
        """

        return password == confirm_password
        
        
    @staticmethod
    def validate_password_format(password):
        """
        Returns a regex search on the password passed as argument,
        to confirm that a user's password contains at least
        8 characters, one number, one uppercase character,
        and a special character. 
        """

        pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        return re.search(pattern, password)

    @staticmethod
    def allowed_file(filename):
        """
        Used when user selects a profile image.
        Ensures that the user isn't able to upload any
        file format other than an image.
        """
        ALLOWED_EXTENSIONS = set(["pdf", "png", "jpg", "jpeg", "gif"])
        if filename != '':
            return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    @staticmethod
    def check_image_filesize(filesize):
        """
        Ensures than an image's filesize can
        be no greater than 500KB.
        """
        max_img_filesize = 0.5 * 1024 * 1024

        if int(filesize) <= max_img_filesize:
            return True
        else:
            return False


    @staticmethod
    def update_profile_image(username, filename,
                         profile_image, updated_info):
        """
        Queries mongoDB "users" collection by matching
        username. And updates profile_image field with
        new profile image filename.

        Saves binary data to mongoDB fs.files and
        fs.chunks collections.
        """

        mongo.save_file(filename, profile_image)
        mongo.db.users.update_one({"username": username},
                                  {"$set": updated_info})

    
    @staticmethod
    def return_profile_image(filename):
        """
        Queries mongoDB files collection to
        send binary data of image. Returns
        the image to be displayed on User's
        profile page, and on Track modals and
        cards in Browse Tracks page.
        """
        try:
            profile_image = mongo.send_file(filename)
        except Exception as e:
            print(f'Error: {e}')

        return profile_image


    @staticmethod
    def check_password(password_hash, password):
        """
        Returns werkzeug.security check_password_hash,
        to ensure that the password submitted matches 
        the encrypted password in mongoDB.
        """
        return check_password_hash(password_hash, password)

    
    @staticmethod
    def delete_user(user_id):
        """
        Queries mongoDB "users" collection by matching ID,
        and removes user document from the collection.
        """

        mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    
    @staticmethod
    def find_file_by_filename(filename):
        """
        Queries mongoDB "fs.files" collection by matching filename,
        and returns the filename found.
        """

        return mongo.db.fs.files.find_one({"filename": filename})


    @staticmethod
    def delete_profileimage_file(_id):
        """
        Queries mongoDB "fs.files" and "fs.chunks" collections,
        and deletes the found filename and binary data.
        """

        mongo.db.fs.files.delete_one({"_id": ObjectId(_id)})
        mongo.db.fs.chunks.delete_one({"files_id": ObjectId(_id)})