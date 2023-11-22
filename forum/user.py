from flask import *
import re

from flask_login import UserMixin, login_manager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from forum.app import db, login_manager, app
from forum.model import User
from forum.utl import username_taken, email_taken, valid_username


# from forum.app import db



@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

#
# password_regex = re.compile("^[a-zA-Z0-9!@#%&]{6,40}$")
# username_regex = re.compile("^[a-zA-Z0-9!@#%&]{4,40}$")
# #Account checks
# def username_taken(username):
#     return User.query.filter(User.username == username).first()
# def email_taken(email):
#     return User.query.filter(User.email == email).first()
# def valid_username(username):
#     if not username_regex.match(username):
#         #username does not meet password reqirements
#         return False
#     #username is not taken and does meet the password requirements
#     return True
# def valid_password(password):
#     return password_regex.match(password)
# #Post checks
# def valid_title(title):
#     return len(title) > 4 and len(title) < 140
# def valid_content(content):
#     return len(content) > 10 and len(content) < 5000

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Text, unique=True)
#     password_hash = db.Column(db.Text)
#     email = db.Column(db.Text, unique=True)
#     admin = db.Column(db.Boolean, default=False)
#     posts = db.relationship("Post", backref="user")
#     comments = db.relationship("Comment", backref="user")
#
#     def __init__(self, email, username, password):
#         self.email = email
#         self.username = username
#         self.password_hash = generate_password_hash(password)
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


@app.route('/action_createaccount', methods=['POST'])
def action_createaccount():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    errors = []
    retry = False
    if username_taken(username):
        errors.append("Username is already taken!")
        retry=True
    if email_taken(email):
        errors.append("An account already exists with this email!")
        retry = True
    if not valid_username(username):
        errors.append("Username is not valid!")
        retry = True
    # if not valid_password(password):
    # 	errors.append("Password is not valid!")
    # 	retry = True
    if retry:
        return render_template("login.html", errors=errors)
    user = User(email, username, password)
    if user.username == "admin":
        user.admin = True
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect("/")

@app.route('/action_login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        login_user(user)
    else:
        errors = []
        errors.append("Username or password is incorrect!")
        return render_template("login.html", errors=errors)
    return redirect("/")


@login_required
@app.route('/action_logout')
def action_logout():
    #todo
    logout_user()
    return redirect("/")

@app.route('/loginform')
def loginform():
    return render_template("login.html")

