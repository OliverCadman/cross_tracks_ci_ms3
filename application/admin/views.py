from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from application.tracks.classes import Track

admin = Blueprint('admin', __name__)

@admin.route("/manage-genres")
def manage_genres():
    """
    Manage genres view

    Queries mongoDB Genre collection for all genres,
    which are passed in to the render_template return
    function, to be rendered onto the 'manage-genres.html'
    """

    # Avoids display of page if any user other than
    # admin attempts to manually enter URL path
    if session["user"] == "admin":

        all_genres = Track.get_genres()
        return render_template('manage-genres.html', all_genres=all_genres)

    else:
        flash("You're not meant to be there!")
        return redirect(url_for("main.index"))

@admin.route("/add-genre", methods=["GET", "POST"])
def add_genre():

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



    
