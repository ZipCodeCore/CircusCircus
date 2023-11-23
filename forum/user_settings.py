from flask import *
import re
from flask_login import UserMixin, current_user, login_manager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forum.app import db, login_manager, app
from forum.model import User
from forum.utl import username_taken, email_taken, valid_username


""" Change Username View
login will be required for the view (request)
Will be a POST method I think, 
need to return to a user settings page - html (to create)
replace login.html render for retry with update user name html (to create)
"""


@login_required
@app.route('/action_change_username', methods=['POST'])
def action_change_username():

    # Get the current user name and desired updated user name from the user_settings form
    current_username = current_user.username
    update_username = request.form['new_username']

    # Check if new user name entered is valid
    errors = []
    retry = False
    if username_taken(update_username):
        errors.append("Username is already taken!")
        retry=True
    if not valid_username(update_username):
        errors.append("Username is not valid!")
        retry = True
    if retry:
        return render_template("user_settings.html", errors=errors)

    # Get current user by using sql alchemy methods
    user = User.query.filter_by(username=current_username).first()

    # (Use sql alchemy session instead?) Update username
    # user.username = update_username

    # Use sql alchemy session method to update username in db
    db.session.execute("UPDATE User SET username = ? WHERE username = ?;", (update_username, user),)

    # Save changes to session db
    db.session.commit()

    # Send the user back to forum page
    # return render_template("user_settings.html", user=current_user)
    return redirect("/")


