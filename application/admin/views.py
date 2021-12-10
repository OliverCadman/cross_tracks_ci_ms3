from flask import (Blueprint, render_template, redirect,
                   url_for, session)
from application.tracks.classes import Track

admin = Blueprint('admin', __name__)

@admin.route("/manage-genres")
def manage_genres():

    all_genres = Track.get_genres()
  

    return render_template('manage-genres.html', all_genres=all_genres )