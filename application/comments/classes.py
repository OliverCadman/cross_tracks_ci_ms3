from application import mongo
import datetime

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
