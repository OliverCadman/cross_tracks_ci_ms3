from os import error
from flask import (Blueprint, render_template, url_for, flash, request, redirect, session, jsonify)
from application.tracks.classes import Track
from application.users.classes import User
from application.comments.classes import Comment
from bson.objectid import ObjectId
import pprint



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
        image_url = request.form.get("image_url")
        added_by = user_id
        
        new_track = Track(track_name, artist_name, album_name,
                          genre, year_of_release, added_by, image_url)

        new_track.add_track()

    return render_template("add-track.html", genres=genres, user_id=user_id)


@tracks.route("/browse-tracks")
def browse_tracks():

    tracks_and_users = Track.bind_users_to_tracks()

    
 
    return render_template("browse-tracks.html", tracks_and_users=tracks_and_users)



@tracks.route('/like-track/<track_id>/<username>')
def like_track(track_id, username):

    selected_track_object = Track.get_track_object(track_id)
    selected_track = selected_track_object._id


    current_user = User.get_user(username)

    if current_user.liked_tracks or current_user.liked_tracks == []:
        users_liked_tracks = current_user.liked_tracks


        if selected_track in users_liked_tracks:
            current_user.remove_liked_track(track_id)
            selected_track_object.remove_like(username)

            return jsonify(num_of_likes=selected_track_object.likes_count, 
                  likes_list=selected_track_object.likes, username=current_user.username)
        else:
            current_user.add_liked_track(track_id)
            selected_track_object.add_like(username)

    
        return jsonify(num_of_likes=selected_track_object.likes_count, 
                  likes_list=selected_track_object.likes, username=username)


@tracks.route("/remove-like/<track_id>/<username>")
def remove_liked_track(track_id, username):

    selected_track_object = Track.get_track_object(track_id)
    selected_track = selected_track_object._id

    current_user = User.get_user(username)

    if current_user.liked_tracks or current_user.liked_tracks == []:

        if selected_track in current_user.liked_tracks:
            current_user.remove_liked_track(track_id)
            selected_track_object.remove_like(username)

    return jsonify(selected_track_object.track_name, current_user.username)


@tracks.route("/add-comment/<track_id>/<username>/", methods=["GET", "POST"])
def add_comment(track_id, username):

    user = User.find_user_by_username(username)
    user_id = user["_id"]

    if request.method == "POST":

        user_input = request.form.get("comment_body")

        if not Comment.check_for_whitespace(user_input):
            error_message = "Your comment is empty!"
            flash(error_message)
            return redirect(url_for("tracks.browse_tracks"))

        new_comment = Comment(user_input, ObjectId(user_id), ObjectId(track_id))
        
        new_comment.add_comment()
        success_message = "Thanks for leaving your comment!"
        flash(success_message)
        return redirect(url_for('tracks.browse_tracks'))


@tracks.route("/edit-track/<track_id>/<username>", methods=["GET", "POST"])
def edit_track(track_id, username):
 

    if request.method == "POST":

        edited_info = {
            "track_name": request.form.get("track_name"),
            "artist_name": request.form.get("artist_name"),
            "album_name": request.form.get("album_name"),
            "genre": request.form.get("genre"),
            "year_of_release": request.form.get("year_of_release"),
            "image_url": request.form.get("image_url")
        }

        Track.edit_track(track_id, edited_info)


    return redirect(url_for('users.user_profile', username=username))


@tracks.route("/delete-track/<track_id>/<username>", methods=["GET", "POST"])
def delete_track(track_id, username):

    # Get Track
    current_track = Track.get_track_id(track_id)
    # Delete track
    
    # Remove track from list of user's liked tracks
    all_users = User.get_all_users()

    # Remove track from comments collection

    if not session["user"]:
        redirect(url_for("users.login"))

    try:
        Track.delete_track(track_id)
    except Exception as e:
        print(e)

    try:
        Comment.delete_track_from_collection(track_id)
    except Exception as e:
        print(e)

    for every_user in all_users:
        # Confirm that 'liked_tracks' field exists in database
        if 'liked_tracks' in every_user:
            User.pull_from_list("liked_tracks", track_id)


    return redirect(url_for('users.user_profile', username=username))







     

    



    
    
