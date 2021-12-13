"""
Comments: Sub-Module

Handles data management and routing when a user
creates, edits or deletes a comment.

Functions:

    add_comment(track_id, username)

    delete_comment(comment_id)

    edit_comment(comment_id)
"""

from flask import (Blueprint, redirect, flash,
                   url_for, request, flash)
from application.comments.classes import Comment
import datetime


comments = Blueprint("comments", __name__)


@comments.route("/add-comment/<track_id>/<username>/", methods=["GET", "POST"])
def add_comment(track_id, username):
    """
    Handles form data submitted from comment form
    in track modals on 'Browse Track' page.

    Checks that the comment is not empty, and
    if so, creates a Comment object, and calls
    on class method 'add_comment()' to insert
    comment into database.

    Parameters:
        track_id
        username
    """

    if request.method == "POST":

        user_input = request.form.get("comment_body")

        if not Comment.check_for_whitespace(user_input):
            error_message = "Your comment is empty!"
            flash(error_message)
            return redirect(url_for("tracks.browse_tracks"))

        new_comment = Comment(user_input, username, track_id)

        new_comment.add_comment()
        success_message = "Thanks for leaving your comment!"
        flash(success_message)
        return redirect(url_for('tracks.browse_tracks'))


@comments.route('/delete_comment/<comment_id>')
def delete_comment(comment_id):
    """
    Invokes Comment class' static method
    "delete_comment", to delete comment
    from comments collection.

    Parameters:
        comment_id
    """

    try:
        Comment.delete_comment(comment_id)

        flash('Comment deleted successfully')
        return redirect(url_for('tracks.browse_tracks'))
    except:
        flash('Sorry, something went wrong. Please try again.')
        return redirect(url_for('tracks.browse-tracks'))


@comments.route('/edit_comment/<comment_id>', methods=["GET", "POST"])
def edit_comment(comment_id):
    """
    Handles form data submitted from comment form
    when user edits their comment. Updates the date
    of original comment added with the date when comment
    is edited, then calls Comment class' static method
    "edit_comment" to update mongoDB "comments" collection.

    Parameters:
        comment_id
    """

    if request.method == "POST":

        input_val = request.form.get('edit_comment')

        date_updated = datetime.datetime.now()

        edited_comment = {
            "comment": input_val,
            "date_added": date_updated
        }

        try:
            Comment.edit_comment(comment_id, edited_comment)

            flash("Comment edited successfully")
            return redirect(url_for('tracks.browse_tracks'))

        except:
            flash("Sorry, something went wrong. Please try again")
            return redirect(url_for('tracks.browse_tracks'))
