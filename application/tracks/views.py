from flask import (Blueprint, render_template, url_for, flash, request, redirect, session, jsonify)
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
        image_url = request.form.get("image_url")
        added_by = user_id
        
        new_track = Track(track_name, artist_name, album_name,
                          genre, year_of_release, added_by, image_url)

        new_track.add_track()

    return render_template("add-track.html", genres=genres, user_id=user_id)


@tracks.route("/browse-tracks")
def browse_tracks():

    tracks_and_users = Track.bind_users_to_tracks()

    print(tracks_and_users)
 
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
    print(track_id, username)


    return redirect(url_for('tracks.browse_tracks'))



    
    
