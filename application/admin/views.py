"""
Admin: Sub-module
========================

Manages the admin views, handling data preparation
and presentation of Track and Genre data.

Views:

    manage_genres()

    manage_tracks()


Functions:

    add_genre()

    delete_genre()
"""


from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from application.tracks.classes import Track


# Initialize admin blueprint
admin = Blueprint('admin', __name__)


@admin.route("/manage-genres")
def manage_genres():
    """
    Manage genres view

    Queries mongoDB Genre collection for all genres,
    which are passed in to the render_template return
    function, to be rendered onto the 'manage-genres.html'

    View only displayed if user 'admin' is logged in.
    """

    if not session.get("user") is None:

        # Avoids display of page if any user other than
        # admin attempts to manually enter URL path
        if session["user"] == "admin":

            all_genres = Track.get_genres()
            return render_template('manage-genres.html', all_genres=all_genres)

        else:
            flash("You're not meant to be there!")
            return redirect(url_for('main.index'))

    else:
        flash("You're not meant to be there!")
        return redirect(url_for("main.index"))


@admin.route("/add-genre", methods=["GET", "POST"])
def add_genre():
    """
    Add Genre Function

    Handles form input in 'manage_genres' view, and
    inserts new genre data into mongoDB 'Genre'
    collection.
    """

    if request.method == "POST":

        genre_name = request.form.get("genre_name")

        if genre_name != '':

            genre_data = {
                "genre_name": genre_name
            }

            try:
                Track.add_genre(genre_data)
                flash("Genre added successfully")
                return redirect(url_for("admin.manage_genres"))

            except:
                flash("Something went wrong. Please try again")
                return redirect(url_for("admin.manage_genres"))

        else:
            flash("No genre name given")
            return redirect(url_for("admin.manage_genres"))


@admin.route("/delete-genre/<genre_id>")
def delete_genre(genre_id):
    """
    Delete Genre View

    Queries mongoDB Genre collection and deletes
    Genre, using genre_id as the argument.
    """

    if session["user"] == "admin":

        try:
            Track.delete_genre(genre_id)
            flash("Genre deleted successfully")
            return redirect(url_for("admin.manage_genres"))
        except:
            flash("Something went wrong. Please try again")
            return redirect(url_for("admin.manage_genres"))


@admin.route("/manage-tracks")
def manage_tracks():

    if not session.get("user") is None:

        if session["user"] == "admin":

            all_tracks = Track.get_all_tracks()
            all_genres = Track.get_genres()

            return render_template("manage-tracks.html", all_tracks=all_tracks,
                                   all_genres=all_genres)

        else:
            flash("You're not meant to be there!")
            return redirect(url_for('main.index'))

    else:
        flash("You're not meant to be there!")
        return redirect(url_for('main.index'))
