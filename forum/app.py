import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user
from forum.models import *
from forum.user import *
from . import create_app


app = create_app()

app.config[''] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///circuscircus.db'
app.config['SITE_NAME'] = 'Schooner'
app.config['SITE_DESCRIPTION'] = 'a schooner forum'
app.config['FLASK_DEBUG'] = 1


def init_site():
	print("creating initial subforums")
	admin = add_subforum("Forum", "Announcements, bug reports, and general discussion about the forum belongs here")
	add_subforum("Announcements", "View forum announcements here",admin)
	add_subforum("Bug Reports", "Report bugs with the forum here", admin)
	add_subforum("General Discussion", "Use this subforum to post anything you want")
	add_subforum("Other", "Discuss other things here")

def add_subforum(title, description, parent=None):
	sub = Subforum(title, description)
	if parent:
		for subforum in parent.subforums:
			if subforum.title == title:
				return
		parent.subforums.append(sub)
	else:
		subforums = Subforum.query.filter(Subforum.parent_id == None).all()
		for subforum in subforums:
			if subforum.title == title:
				return
		db.session.add(sub)
	print("adding " + title)
	db.session.commit()
	return sub

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

with app.app_context():
	load_db()
	db.create_all()
	if not Subforum.query.all():
		init_site()

 
@app.route('/')
def index():
	subforums = Subforum.query.filter(Subforum.parent_id == None).order_by(Subforum.id)
	return render_template("subforums.html", subforums=subforums)




