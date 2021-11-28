from flask import (Blueprint, render_template, redirect, flash, url_for, session, jsonify, request, flash)
from application.comments.classes import Comment
import urllib

comments = Blueprint("comments", __name__)

@comments.route('/delete_comment/<comment_id>')
def delete_comment(comment_id):

    print(comment_id)

    try:
        Comment.delete_comment(comment_id)
        
        flash('Comment deleted successfully')
        return redirect(url_for('tracks.browse_tracks'))
    except:
        flash('Sorry, something went wrong. Please try again.')
        return redirect(url_for('tracks.browse-tracks'))

@comments.route('/edit_comment/<comment_id>', methods=["GET", "POST"])
def edit_comment(comment_id):


    if request.method == "POST":

        input_val = request.form.get('edit_comment')

        edited_comment = {
            "comment": input_val
        }

        try:
            Comment.edit_comment(comment_id, edited_comment)

            flash("Comment edited successfully")
            return redirect(url_for('tracks.browse_tracks'))

        except Exception as e:
            print(e)
            flash("Sorry, something went wrong. Please try again")
            return redirect(url_for('tracks.browse_tracks'))




    



    

