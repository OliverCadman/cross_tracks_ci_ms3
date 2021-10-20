from flask import (Blueprint, render_template, url_for, flash, request, session)
from application.tracks.classes import Track
from application.users.classes import User

tracks = Blueprint("tracks", __name__)

@tracks.route("/add-track/<username>", methods=["GET","POST"])
def add_track(username):

    user_id = User.get_id(username)
    genres = Track.get_genres()

    if request.method == "POST":

        track_name = request.form.get("track_name")
        artist_name = request.form.get("artist_name")
        album_name = request.form.get("album_name")
        genre = request.form.get("genre")
        year_of_release = request.form.get("year_of_release")
        added_by = user_id
        
        new_track = Track(track_name, artist_name, album_name,
                          genre, year_of_release, added_by)

        new_track.add_track()

    return render_template("add-track.html", genres=genres, user_id=user_id)
