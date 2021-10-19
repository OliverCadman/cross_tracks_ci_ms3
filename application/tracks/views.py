from flask import (Blueprint, render_template, url_for, flash, request, session)
from application.tracks.classes import Track

tracks = Blueprint("tracks", __name__)

@tracks.route("/add-track")
def add_track():
    return render_template("add-track.html")
