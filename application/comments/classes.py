"""
Comment Class
=============

Handles CRUD operations concerning comments
left in track modals on 'Browse Tracks' page.

Classes: Comment
"""

from application import mongo
from bson.objectid import ObjectId
import datetime
import re


class Comment:
    """
    Class to represent a comment.
    A comment object is created through user
    submission in track modals in Browse Tracks
    page, and inserted into mongoDB 'comments' collection
    using class methods 'get_comment_info' and 'add_comment'.

    Additional static methods handle comment validation,
    editing, deleting, and joining to 'user' collection.


    Attributes:

        comment_body: str
            The comment itself

        comment_author: str
            The username of the user who left the comment

        track_id: str
            The id of the track the comment is concerning

        _id: str
            The id of the comment itself


    Instance Methods:

        get_comment_info()
            Collects and prepares data when comment object created,
            to insert into mongoDB 'comments' collection.

        add_comment()
            Invokes get_comment_info() method and inserts
            data into mongoDB 'comments' collection.


    Static Methods:

        check_for_whitespace(comment)
            Uses regex compile and match methods to
            check if the submitted comment is empty.

        bind_users_to_comments()
            Uses mongoDB aggregate 'lookup' method
            to join users to comments, using local field
            "author" as reference to foreign field
            "_id" in user collection.

        delete_track_from_collection(track_id):
            Deletes all comments related to a particular track,
            in the case when the track is deleted, or a user
            deletes their account.

        delete_comment(comment_id):
            Deletes comment from mongoDB 'comments' collection.

        edit_comment(comment_id, comment_content):
            Updates mongoDB 'comments' collection with edited
            comment.
    """

    def __init__(self, comment_body, comment_author,
                 track_id, _id=None):
        """
        Constructor to create attributes attributable to comment object.
        """

        self.comment_body = comment_body
        self.comment_author = comment_author
        self.track_id = ObjectId(track_id)
        self._id = _id if isinstance(_id, str) else ""

    def get_comment_info(self):
        """
        Gathers and prepares data, ready to be inserted
        into mongoDB "comments" collection.
        """

        date_added = datetime.datetime.now()

        comment_info = {
            "comment": self.comment_body,
            "author": self.comment_author,
            "track_id": self.track_id,
            "date_added": date_added
        }

        return comment_info

    def add_comment(self):
        """
        Invokes class method get_comment_info,
        and inserts returned data into mongoDB
        "comments" collection.
        """

        comment = self.get_comment_info()

        if comment is not None:
            mongo.db.comments.insert_one(comment)
        else:
            return False

    @staticmethod
    def check_for_whitespace(comment):
        """
        Uses regex compile and match methods to
        check if the submitted comment is empty,
        returning the value, accessed in
        comment view.
        """

        regex_pattern = re.compile("(.|\s)*\S(.|\s)*")
        whitespace_check = re.match(regex_pattern, comment)

        return whitespace_check

    @staticmethod
    def bind_users_to_comments():
        """
        Aggregate "lookup" to join comments
        and users collection, using local field
        "author" as reference to foreign field
        "_id" in user collection.
        """

        return mongo.db.comments.aggregate([
            {
                "$lookup": {
                    "from": "users",
                    'localField': "author",
                    'foreignField': "_id",
                    'as': 'author'
                }
            }
        ])

    @staticmethod
    def delete_track_from_collection(track_id):
        """
        Deletes all comments related to a particular track,
        in the case when the track is deleted, or a user
        deletes their account.
        """

        mongo.db.comments.delete_many(
            {"track_id": ObjectId(track_id)})

    @staticmethod
    def delete_comment(comment_id):
        """
        Deletes comment from mongoDB 'comments' collection.
        """

        mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})

    @staticmethod
    def edit_comment(comment_id, comment_content):
        """
        Updates mongoDB 'comments' collection with edited
        comment.
        """

        mongo.db.comments.update_one({"_id": ObjectId(comment_id)},
                                     {"$set": comment_content})
