import datetime

from flask import *
import re
from flask_login import UserMixin, current_user, login_manager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forum.app import db, login_manager, app
from forum.model import User, Post, Comment, Message
from sqlalchemy import select, func
from forum.utl import username_taken, email_taken, valid_username

""" View own profile, changing settings available """
@login_required
@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    user_id = current_user.id
    posts = Post.query.filter_by(user_id=user_id).all()
    comments = Comment.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', user=user, posts=posts, comments=comments, titleFunc=get_post_title, countFunc=get_count)


""" View another users profile """
@login_required
@app.route('/profile/<username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    posts = Post.query.filter_by(user_id=user_id).all()
    comments = Comment.query.filter_by(user_id=user_id).all()
    return render_template('viewprofile.html', user=user, posts=posts, comments=comments, titleFunc=get_post_title, countFunc2=get_count2)


""" Function to get post title for a comment, used in comment title in profile.html """
def get_post_title(post_id):
    comment_post = db.session.query(Post).filter(Post.id == post_id).first()
    comment_post_title = comment_post.title
    return comment_post_title


""" Function to get the count of a type of forum message for users profile """


def get_count(count_type):
    if count_type == "post":
        count = Post.query.filter_by(user_id=current_user.id).count()
    elif count_type == "comment":
        count = Comment.query.filter_by(user_id=current_user.id).count()
    else:
        count = 0
    return count


""" Function to get the count of a type of forum message when viewing other users profiles"""


def get_count2(count_type, user_id):
    if count_type == "post":
        count = Post.query.filter_by(user_id=user_id).count()
    elif count_type == "comment":
        count = Comment.query.filter_by(user_id=user_id).count()
    else:
        count = 0
    return count


""" View to the send direct message page for a user profile """
@login_required
@app.route('/profile/<recipient>/send_message')
def send_message(recipient):
    return render_template('send_message.html', recipient=recipient)


""" View to send the direct message to the user """

@login_required
@app.route('/profile/send_message/send', methods=['POST'])
def send_the_message():
    recipient = request.args.get("recipient")
    user = User.query.filter_by(username=recipient).first()
    content = request.form['content']
    postdate = datetime.datetime.now()
    message = Message(content=content, postdate=postdate)
    current_user.messages_sent.append(message)
    user.messages_received.append(message)
    db.session.commit()
    return redirect("/")

""" View for viewing direct messages """
@login_required
@app.route('/user/view_messages')
def view_messages():
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    received_messages = user.messages_received
    # sender_names = []

    # Get the sender name to print with the message content on page
    for message in received_messages:
        sender_id = message.sender_id
        sender_name = User.query.filter_by(id=sender_id).first().username
        message.sender_name = sender_name
        # sender_names.append(sender_name)

    return render_template('viewmessages.html', received_messages=received_messages)