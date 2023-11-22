import re

from forum.model import User


def error(errormessage):
	return "<b style=\"color: red;\">" + errormessage + "</b>"


password_regex = re.compile("^[a-zA-Z0-9!@#%&]{6,40}$")
username_regex = re.compile("^[a-zA-Z0-9!@#%&]{4,40}$")
#Account checks
def username_taken(username):
    return User.query.filter(User.username == username).first()
def email_taken(email):
    return User.query.filter(User.email == email).first()
def valid_username(username):
    if not username_regex.match(username):
        #username does not meet password reqirements
        return False
    #username is not taken and does meet the password requirements
    return True
def valid_password(password):
    return password_regex.match(password)
#Post checks
def valid_title(title):
    return len(title) > 4 and len(title) < 140
def valid_content(content):
    return len(content) > 10 and len(content) < 5000