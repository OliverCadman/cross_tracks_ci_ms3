"""
Track Class
==============

Handles all track data that will be created, read, 
updated and deleted using MongoDB. 

"""

from application import mongo
from bson.objectid import ObjectId
import datetime


class Track:

    def __init__(self, track_name, artist_name, album_name,
                 genre, year_of_release, added_by, image_url=None,
                 likes=None, likes_count=None, _id=None, date_added=None):


        self._id = _id
        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.genre = genre
        self.year_of_release = year_of_release
        self.added_by = added_by
        self.image_url = image_url if isinstance(image_url, str) else str("")
        self.likes = likes if isinstance(likes, list) else []
        self.likes_count = likes_count if isinstance(likes_count, int) else 0
        self.date_added = date_added if isinstance(date_added, str) else None

    
    def get_track_info(self):

        date_added = datetime.datetime.now()

        track_info = {
            "track_name": self.track_name,
            "artist_name": self.artist_name,
            "album_name": self.album_name,
            "genre": self.genre,
            "added_by": self.added_by,
            "year_of_release": self.year_of_release,
            "image_url": self.image_url,
            "likes": self.likes,
            "likes_count": self.likes_count,
            "date_added": date_added
            }

        return track_info

    
    def add_track(self):

        """
        TODO: Add conditional to query mongoDB for track, to determine if it is already
        in the database.
        """

        track_data = self.get_track_info()

        mongo.db.tracks.insert(track_data)

    @staticmethod
    def edit_track(track_id, track_data):
        
        try:
            mongo.db.tracks.update_one(
                {"_id": ObjectId(track_id)},
                {"$set": track_data})

        except Exception as e:
            print(e)

        
    def get_artist_name(self):

        artist_name = self.artist_name

        mongo.db.tracks.find_one({"artist_name": artist_name})

    
    def get_track_name(self):

        track_name = self.track_name


    def add_like(self, username):

        self.likes.append(username)

        self.likes_count += 1

        mongo.db.tracks.update_one({
            "_id": self._id},
            {"$set": self.get_track_info()}
        )


    def remove_like(self, username):

        if username in self.likes:
            print("username:", username)
            self.likes.remove(username)

            self.likes_count -= 1

            mongo.db.tracks.update_one({
            "_id": self._id},
            {"$set": self.get_track_info()})

            return True
        else:
            return False


    @staticmethod
    def get_track_id(id):
        return mongo.db.tracks.find_one({"_id": ObjectId(id)})


    @classmethod
    def get_track_object(cls, _id):

        if ObjectId().is_valid(_id):
            data = mongo.db.tracks.find_one({"_id": ObjectId(_id)})

        if data is not None:
            return cls(**data)
        else:
            data = None
            return False

    
    @staticmethod
    def get_genres():

        genres = mongo.db.genres.find().sort("genre_name", 1)
        return genres

    @staticmethod
    def get_users_tracks(id):

        if ObjectId.is_valid(id):
            users_tracks = mongo.db.tracks.find({"added_by": ObjectId(id)})
            # Return cursor only if it contains data
            if users_tracks.count() > 0:
                return users_tracks
        else:
            return False

    @staticmethod
    def get_all_tracks():

        return mongo.db.tracks.find()

    @staticmethod
    def get_latest_tracks():

        return mongo.db.tracks.find().sort("_id", -1).limit(6)

    @staticmethod 
    def bind_users_to_tracks():

        return mongo.db.tracks.aggregate([
            {
                "$lookup": {
                    "from": "users",
                    'localField': "added_by",
                    'foreignField': "_id",
                    'as': 'user'
                }
            }, {
                "$lookup": {
                    "from": "comments",
                    "localField": "_id",
                    "foreignField": "track_id",
                    "as": "comments"
                },
            }, 
            {
                "$lookup": {
                    "from": "users",
                    "localField": "comments.author",
                    "foreignField": "_id",
                    "as": "comment_added_by"
                }
            }
        ])

    
    @staticmethod
    def bind_users_to_comments():

        return mongo.db.comments.aggregate([
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "user_details"
                }},

                { "$lookup": {
                    "from": "comments",
                    "localField": "_id",
                    "foreignField": "track_id",
                    "as": "comments"
                }},
            
        ])



    








        









    