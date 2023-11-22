
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login.utils import login_required
from flask_login import current_user

from .models import User

import re

password_regex = re.compile("^[a-zA-Z0-9!@#%&]{6,40}$")
username_regex = re.compile("^[a-zA-Z0-9!@#%&]{4,40}$")
#Account checks
def valid_username(username):
	if not username_regex.match(username):
		#username does not meet password reqirements
		return False
	#username is not taken and does meet the password requirements
	return True
def valid_password(password):
	return password_regex.match(password)

def username_taken(username):
	return User.query.filter(User.username == username).first()
def email_taken(email):
	return User.query.filter(User.email == email).first()
