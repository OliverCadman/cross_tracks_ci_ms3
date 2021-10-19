"""
Track Class
==============

Handles all track data that will be created, read, 
updated and deleted using MongoDB. 

"""

class Track:

    def __init__(self, track_name, artist_name, album_name,
                 genre, added_by, year_of_release, 
                 likes=None, like_count=None):


        self.track_name = track_name
        self.artist_name = artist_name
        self.album_name = album_name
        self.genre = genre
        self.added_by = added_by
        self.year_of_release = year_of_release
        self.likes = likes if isinstance(likes, list) else []
        self.like_count = like_count if isinstance(like_count, int) else 0

        

    