"""
Track Class
===========

Handles all track data that will be created, read,
updated and deleted using MongoDB.

Classes: Track
"""

from application import mongo
from bson.objectid import ObjectId
import datetime
import json
from bson.json_util import loads, dumps


class Track:
    """
    Class to represent a Track.
    Handles all methods to store, edit, join,
    read and delete data in mongoDB track collection.

    The initial track object is created upon submission
    of form in "Add a Track" page.

    Attributes:

        _id: str
            The unique identifier for the track.

        track_name: str
            The name of the track being added.

        artist_name: str
            The name of the artist who composed the track.

        album_name: str
            The name of the album that the track is
            featured on.

        genre: str
            The name of the genre of the track.

        year_of_release: int
            The year the track was released.

        added_by: str
            The username of the user who added
            the track.

        image_url: str (optional)
            The image address of the album/single
            art of the relative track.

        likes: list (optional)
            A list of users who have 'liked' the
            track.

        likes_count: int (optional)
            The number of likes attributed to
            the track.


    Instance methods:

        get_track_info(self):
            Prepares data created from Track object
            into dictionary, ready to be inserted
            into mongoDB 'tracks' collection.

        add_track(self):
            Invokes 'get_track_info()' method,
            and inserts returned value into
            mongoDB 'tracks' collection.

        add_like(self, username)
            Adds username who liked the track into
            the track document's 'likes' list, and
            increments the same document's 'likes'
            count.

        remove_like(self, username)
            Removes username who liked the track from
            the track document's 'likes' list, and
            decrements the same document's 'likes'
            count.


    Class methods:

        get_track_object(cls, _id)
            Creates a track object upon retrieval of
            track document from mongoDB 'tracks' collection.
            Utilised by add_like() and remove_like() instance
            methods.


    Static methods:

            edit_track(track_id, track_data)
                Handles form input, and queries mongoDB
                'tracks' collection by track_id, and updates
                the returned track  document with updated track data.

            delete_track(track_id)
                Queries mongoDB 'tracks' collection
                by track_id, and deletes track.

            add_genre(genre_data)
                Handles form input in admin 'Manage Genres' view,
                and adds genre to mongoDB 'genres' collection.

            delete_genre(genre_id)
                Queries mongoDB 'genres' collection
                by genre_id, and deletes genre.

            get_genres()
                Queries mongoDB 'genre' collection, and returns
                all genres.

            get_users_tracks(id)
                Queries mongoDB 'tracks' collection, and returns
                all tracks that are attributed to user's id.

            get_all_tracks()
                Queries mongoDB 'tracks' collection,
                and returns all tracks.

            get_latest_tracks()
                Queries mongoDB 'tracks' collection,
                joined to 'users' and 'comments' collection.
                Returns tracks, limited to the last 6
                documents that have been added.

            bind_users_to_tracks()
                Queries mongoDB 'tracks' collection,
                joined to 'users' and 'comments' collection.
                Returns all tracks.

            remove_user_from_likes_list(username)
                Queries mongoDB 'tracks' collection,
                finding all instances of username
                in 'likes_list' of all tracks, and
                removes the same username from all
                'likes' lists.

            decrement_likes_count(username)
                Decrements likes_count of all tracks
                where username is found in the same
                document's 'likes_list'.

            delete_users_tracks(user_id)
                Deletes all track documents attributed
                to a particular user.

            search_tracks(query)
                Searches tracks using query string passed
                in as the argument.

            parse_json()
                Parses json data so it can be handled by
                flask's 'jsonify' method, when making
                AJAX calls.
    """

    def __init__(self, track_name, artist_name, album_name,
                 genre, year_of_release, added_by, image_url=None,
                 likes=None, likes_count=None, _id=None, date_added=None):

        """
        Constructor to create attributes, attributable to Track object.
        """

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

    def get_track_info(self):

        """
        Gathers and prepares data, ready to be inserted
        into mongoDB "comments" collection.

        Returns data to be handled by "add_track" method.
        """

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
            }

        return track_info

    def add_track(self):

        """
        Invokes Track Class instance method
        "get_track_info()", and inserts
        returned value into mongoDB "tracks"
        collection.
        """

        track_data = self.get_track_info()

        mongo.db.tracks.insert(track_data)

    @staticmethod
    def edit_track(track_id, track_data):

        """
        Handles form input, and queries mongoDB
        'tracks' collection by track_id, and updates
        the returned track  document with updated track data.
        """

        try:
            mongo.db.tracks.update_one(
                {"_id": ObjectId(track_id)},
                {"$set": track_data})

        except Exception as e:
            print(e)

    @staticmethod
    def delete_track(track_id):
        """
        Queries mongoDB 'tracks' collection
        by track_id, and deletes track.
        """

        mongo.db.tracks.delete_one({"_id": ObjectId(track_id)})

    def add_like(self, username):
        """
        Adds username who liked the track into
        the track document's 'likes' list, and
        increments the same document's 'likes'
        count.
        """

        self.likes.append(username)

        self.likes_count += 1

        mongo.db.tracks.update_one({
            "_id": self._id},
            {"$set": self.get_track_info()}
        )

    def remove_like(self, username):
        """
        Used in conjunction with "get_track_object()"
        class method.

        Removes username who liked the track from
        the track document's "likes" list (if
        username is found in "likes" list), and
        decrements the same document's "likes"
        count.

        Updates mongoDB tracks collection with
        updated data using "get_track_info()"
        instance method.
        """

        if username in self.likes:
            self.likes.remove(username)

            self.likes_count -= 1

            mongo.db.tracks.update_one({
                            "_id": self._id},
                            {"$set": self.get_track_info()})

            return True
        else:
            return False

    @classmethod
    def get_track_object(cls, _id):
        """
        Creates a track object upon retrieval of
        track document from mongoDB 'tracks' collection.
        Utilised by add_like() and remove_like() instance
        methods.
        """

        if ObjectId().is_valid(_id):
            data = mongo.db.tracks.find_one({"_id": ObjectId(_id)})

        if data is not None:
            return cls(**data)
        else:
            data = None
            return False

    @staticmethod
    def get_genres():
        """
        Queries mongoDB 'genre' collection, and returns
        all genres.
        """

        genres = mongo.db.genres.find().sort("genre_name", 1)
        return genres

    @staticmethod
    def add_genre(genre_data):
        """
        Handles form input in admin 'Manage Genres' view,
        and adds genre to mongoDB 'genres' collection.
        """

        mongo.db.genres.insert_one(genre_data)

    @staticmethod
    def delete_genre(genre_id):
        """
        Queries mongoDB 'genres' collection
        by genre_id, and deletes genre.
        """

        mongo.db.genres.delete_one({"_id": ObjectId(genre_id)})

    @staticmethod
    def get_users_tracks(id):
        """
        Queries mongoDB 'tracks' collection, and returns
        all tracks that are attributed to user's id.
        """

        if ObjectId.is_valid(id):
            users_tracks = mongo.db.tracks.find({"added_by": ObjectId(id)})
            # Return cursor only if it contains data
            if users_tracks.count() > 0:
                return users_tracks
        else:
            return False

    @staticmethod
    def get_all_tracks():
        """
        Queries mongoDB 'tracks' collection,
        and returns all tracks.
        """

        return mongo.db.tracks.find()

    @staticmethod
    def get_latest_tracks():
        """
        Queries mongoDB 'tracks' collection,
        joined to 'users' and 'comments' collection.
        Returns tracks, sorted in reverse by ObjectId,
        and limited to the last 6 documents that
        have been added.
        """

        return mongo.db.tracks.aggregate([
            {
                "$lookup": {
                    "from": "users",
                    "localField": "added_by",
                    "foreignField": "_id",
                    "as": "user"
                }
            }, {
                "$lookup": {
                    "from": "comments",
                    "localField": "_id",
                    "foreignField": "track_id",
                    "as": "comments"

                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "comments.author",
                    "foreignField": "_id",
                    "as": "comment_added_by"
                }
            },
            {"$sort": {"_id": -1}},
            {"$limit": 6}
        ])

    @staticmethod
    def bind_users_to_tracks():
        """
        Queries mongoDB 'tracks' collection,
        joined to 'users' and 'comments' collection.
        Returns all tracks.
        """

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
    def delete_users_tracks(user_id):
        """
        Deletes all track documents attributed
        to a particular user.
        """

        mongo.db.tracks.delete_many({"added_by": ObjectId(user_id)})

    @staticmethod
    def remove_user_from_likes_list(username):
        """
        Queries mongoDB 'tracks' collection,
        finding all instances of username
        in 'likes_list' of all tracks, and
        removes the same username from all
        'likes' lists.
        """

        mongo.db.tracks.update_many({"likes": username},
                                    {"$pull": {"likes": username}})

    @staticmethod
    def decrement_likes_count(username):
        """
        Decrements likes_count of all tracks
        where username is found in the same
        document's 'likes_list'.
        """

        mongo.db.tracks.update_many({
            "likes": username},
            {"$inc": {"likes_count": -1}})

    @staticmethod
    def search_tracks(query):
        """
        Searches tracks using query string passed
        in as the argument. Returns a list of tracks
        where data matches the given query string.
        """

        return list(mongo.db.tracks.find({"$text": {"$search": query}}))

    @staticmethod
    def parse_json(data):
        """
        Parses json data so it can be handled by
        flask's 'jsonify' method, when making
        AJAX calls.
        """

        return json.loads(dumps(data))
