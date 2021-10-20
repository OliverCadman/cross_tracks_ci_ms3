from flask import (Blueprint, render_template, url_for, flash, request, session)
from application.tracks.classes import Track
from application.users.classes import User

tracks = Blueprint("tracks", __name__)

@tracks.route("/add-track/<username>", methods=["GET","POST"])
def add_track(username):

    user_id = User.get_id(username)
    genres = Track.get_genres()

    return render_template("add-track.html", genres=genres, user_id=user_id)
