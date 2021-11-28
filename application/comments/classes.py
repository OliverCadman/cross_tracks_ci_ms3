from application import mongo
from bson.objectid import ObjectId
import datetime
import re

class Comment:

    def __init__(self, comment_body, comment_author, track_id, _id=None):

        self.comment_body = comment_body
        self.comment_author = comment_author
        self.track_id = track_id
        self._id = _id if isinstance(_id, str) else ""

    
    def get_comment_info(self):

        date_added = datetime.datetime.now()

        comment_info = {
            "comment": self.comment_body,
            "author": self.comment_author,
            "track_id": self.track_id,
            "date_added": date_added
        }

        return comment_info

    
    def get_comment_info(self):

        date_added = datetime.datetime.now()

        comment_info = {
            "comment": self.comment_body,
            "author": self.comment_author,
            "track_id": self.track_id,
            "date_added": date_added
        }

        return comment_info

    
    def add_comment(self):


        comment = self.get_comment_info()

        if comment:
            try:
                mongo.db.comments.insert_one(comment)
            except:
                print('Server error, unable to insert document')

    @staticmethod
    def check_for_whitespace(comment):

        regex_pattern = re.compile("(.|\s)*\S(.|\s)*")
        whitespace_check = re.match(regex_pattern, comment)

        return whitespace_check


    @staticmethod 
    def bind_users_to_comments():

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

        mongo.db.comments.delete_many({"track_id": ObjectId(track_id)})
        

    @staticmethod
    def delete_comment(comment_id):

        mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})

    
    @staticmethod
    def edit_comment(comment_id, comment_content):

        mongo.db.comments.update_one({"_id": ObjectId(comment_id)},
                                     {"$set": comment_content})

