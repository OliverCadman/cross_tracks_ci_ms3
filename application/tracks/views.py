"""
Tracks: Sub-module

Handles all routing and data preparation
relative to tracks.

Views:
    add_track(username)

    browse_tracks()

Functions:
    like_track()

    remove_liked_track()

    edit_track()

    delete_track()

    search_track()
"""


from os import error
from flask import (Blueprint, render_template, url_for,
                   flash, request, redirect, session, jsonify, abort)
from application.tracks.classes import Track
from application.users.classes import User
from application.comments.classes import Comment
from bson.objectid import ObjectId
from application import mongo
from flask_paginate import Pagination, get_page_args
import pprint


tracks = Blueprint("tracks", __name__)


@tracks.route("/add-track/<username>", methods=["GET", "POST"])
def add_track(username):
    """
    Renders 'add-track.html' template.

    Invokes Track classes' "get_genres()" method,
    to be accessed in select dropdown in form.

    Invokes User classes' "get_id" method, to
    insert user's id to be used as a foreign key
    when joining 'tracks' and 'users' collections.

    Handles data submitted through form
    in 'add-track.html', and creates Track object,
    which is inserted into mongoDB 'tracks' collection.
    """

    # Customised error handling in case of invalid URL path
    if User.find_user_by_username(username) is None:
        abort(404)

    user_id = User.get_id(username)
    genres = Track.get_genres()

    if request.method == "POST":

        track_name = request.form.get("track_name")
        artist_name = request.form.get("artist_name")
        album_name = request.form.get("album_name")
        genre = request.form.get("genre")
        year_of_release = request.form.get("year_of_release")
        image_url = request.form.get("image_url")
        added_by = user_id

        # Grabs value from initial option
        # in select dropdown, 'Choose a Genre:'
        # Genre name defaults to 'N/A' if not selected.
        if genre == '':
            genre = 'N/A'

        try:
            # Create Track object
            new_track = Track(track_name, artist_name, album_name,
                              genre, year_of_release, added_by, image_url)

            # Instance method of Track object
            new_track.add_track()
            flash('Track added successfully')
            return redirect(url_for('tracks.browse_tracks', username=username))
        except:
            flash('Sorry, something went wrong. Please try again')
            return redirect(url_for('tracks.add_track', username=username))

    return render_template("add-track.html", genres=genres, user_id=user_id)


@tracks.route("/browse-tracks", methods=["GET", "POST"])
def browse_tracks():
    """
    Renders 'browse-tracks.html' template.
    """

    latest_tracks = Track.get_latest_tracks()
    genres = Track.get_genres()
    all_users = User.get_all_users()

    user_list = []
    for user in all_users:
        user_list.append(user["username"])

    genre_list = []
    for genre in genres:
        genre_list.append(genre["genre_name"])

    if request.headers.get("Content-Type") == "application/json":
        return jsonify(genre_list=genre_list, user_list=user_list)

    tracks_to_paginate = Track.get_all_tracks()
    paginated_tracks = Track.paginate(tracks_to_paginate)
    pagination = Track.pagination_args(tracks_to_paginate)

    return render_template("browse-tracks.html",
                           all_tracks_list=paginated_tracks,
                           latest_tracks=latest_tracks,
                           genre_list=genre_list,
                           pagination=pagination)


@tracks.route('/like-track/<track_id>/<username>')
def like_track(track_id, username):
    """
    Handles user input when user clicks the star
    displayed on each track card in browse tracks page.

    Invokes Track class' 'get_track_object' method,
    to access the relative instance methods.


    In the case where the particular track isn't found in
    the user's 'liked_tracks' list, the method 'add_like'
    is invoked. If the track is found in the user's
    'liked_tracks' list, then the 'remove_like' instance
    method is invoked.

    Returns jsonify, used in conjunction with AJAX call in
    'like-button-ajax.js' found in static/js directory.
    """

    selected_track_object = Track.get_track_object(track_id)
    selected_track = selected_track_object._id

    current_user = User.get_user(username)

    users_liked_tracks = current_user.liked_tracks

    if selected_track in users_liked_tracks:

        current_user.remove_liked_track(track_id)
        selected_track_object.remove_like(username)

        return jsonify(num_of_likes=selected_track_object.likes_count,
                       likes_list=selected_track_object.likes,
                       username=current_user.username)
    else:
        try:
            current_user.add_liked_track(track_id)
            selected_track_object.add_like(username)
        except Exception as e:
            print(e)

        return jsonify(num_of_likes=selected_track_object.likes_count,
                       likes_list=selected_track_object.likes,
                       username=username)


@tracks.route("/remove-like/<track_id>/<username>")
def remove_liked_track(track_id, username):
    """
    Function utilised in 'User Profile' page, when
    user removes track from their 'Liked Tracks'
    collection.

    Invokes Track class' 'get_track_object' method,
    to access the relative instance methods.

    Invokes User class static method 'get_user',
    to be used to check if track is in user's
    "liked_tracks" list.

    Returns jsonify, in conjunction with AJAX call in
    'remove-like-ajax.js' found in static/js directory.
    """

    selected_track_object = Track.get_track_object(track_id)
    selected_track = selected_track_object._id

    current_user = User.get_user(username)

    if current_user.liked_tracks or current_user.liked_tracks == []:

        if selected_track in current_user.liked_tracks:
            current_user.remove_liked_track(track_id)
            selected_track_object.remove_like(username)

    parsed_track_id = Track.parse_json(current_user.liked_tracks)

    return jsonify(track_name=selected_track_object.track_name,
                   username=current_user.username,
                   liked_tracks=parsed_track_id)


@tracks.route("/edit-track/<track_id>", methods=["GET", "POST"])
def edit_track(track_id):
    """
    Handles data submitted through form
    in modal window in "browse-tracks.html"
    and "user-profile.html".

    Once data is prepared into dictionary,
    the Track class static method "edit_track()"
    is invoked.
    """

    if request.method == "POST":

        edited_info = {
            "track_name": request.form.get("track_name"),
            "artist_name": request.form.get("artist_name"),
            "album_name": request.form.get("album_name"),
            "genre": request.form.get("genre"),
            "year_of_release": request.form.get("year_of_release"),
            "image_url": request.form.get("image_url")
        }

        try:
            Track.edit_track(track_id, edited_info)
            flash('Track edited successfully')
            return redirect(request.referrer)
        except:
            flash('Sorry, there was a problem. Please try again.')
            return redirect(request.referrer)


@tracks.route("/delete-track/<track_id>/<username>", methods=["GET", "POST"])
def delete_track(track_id, username):
    """
    Handles deletion of track, and removal of track data
    in "tracks" and "users" collections.
    """

    # Remove track from list of user's liked tracks
    all_users = User.get_all_users()

    # Remove track from comments collection

    if not session["user"]:
        redirect(url_for("users.login"))

    try:
        Track.delete_track(track_id)
        Comment.delete_track_from_collection(track_id)

        for every_user in all_users:
            # Confirm that 'liked_tracks' field exists in database
            if 'liked_tracks' in every_user:
                User.pull_from_list("liked_tracks", track_id)

        flash('Track deleted successfully')
        return redirect(request.referrer)
    except:
        flash('Sorry, something went wrong. Please try again.')
        return redirect(request.referrer)


@tracks.route("/search-track", methods=["GET", "POST"])
def search_track():
    """
    Handles user input in search window
    in "browse-tracks.html".

    Used in conjunction with AJAX call.

    Returned data is 'jsonified', so it
    can be utilised in the 'success' response
    in AJAX call, and rendered asynchronously.
    """

    query = None
    if request.method == "POST":

        # Utilising data passed from AJAX call
        query = str(request.get_data())

        results = Track.search_tracks(query)

        results_list = []
        if results:
            for result in results:
                json_encoded_result = Track.parse_json(result)
                results_list.append(json_encoded_result)

            return jsonify(results_list=results_list)

        else:
            new_results_list = []
            return jsonify(new_results_list=new_results_list)
