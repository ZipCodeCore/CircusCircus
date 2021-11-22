from flask import *
#from flask.ext.login import LoginManager, login_required, current_user, logout_user, login_user
from flask_login import LoginManager, current_user, login_user, logout_user
import datetime
import sys

from flask_login.utils import login_required
from sqlalchemy.sql.elements import Null
from forum.app import app
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
import re
import datetime
from flask_login.login_manager import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(app)

#VIEWS

@app.route('/')
def index():
	subforums = Subforum.query.filter(Subforum.parent_id == None).order_by(Subforum.id)
	return render_template("subforums.html", subforums=subforums)

@app.route('/subforum')
def subforum():
	subforum_id = int(request.args.get("sub")) 
	subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
	if not subforum:
		return error("That subforum does not exist!")
	posts = Post.query.filter(Post.subforum_id == subforum_id).order_by(Post.id.desc()).limit(50)
	if not subforum.path:
		subforum.path = generateLinkPath(subforum.id)

	subforums = Subforum.query.filter(Subforum.parent_id == subforum_id).all()
	return render_template("subforum.html", subforum=subforum, posts=posts, subforums=subforums, path=subforum.path)

@app.route('/loginform')
def loginform():
	return render_template("login.html")

@login_required
@app.route('/userinfo')
def userinfo():
	return render_template("userinfo.html")

@login_required
@app.route('/addpost')
def addpost():
	subforum_id = int(request.args.get("sub"))
	subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
	if not subforum:
		return error("That subforum does not exist!")

	return render_template("createpost.html", subforum=subforum)


#Wes Work Begin
@login_required
@app.route('/privatepost')
def privatepost():
	subforum_id = int(request.args.get("sub"))
	subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
	if not subforum:
		return error("That subforum does not exist!")

	return render_template("privatepost.html", subforum=subforum)
#Wes Work End


@login_required
@app.route('/viewpost')
def viewpost():
	postid = int(request.args.get("post")) # provides dictionary of the post table
	post = Post.query.filter(Post.id == postid).first()
	if not post:
		return error("That post does not exist!")
	if not post.subforum.path:
		subforum.path = generateLinkPath(post.subforum.id)
	comments = Comment.query.filter(Comment.post_id == postid).order_by(Comment.id.desc()) # no need for scalability now
	newdict = {}
	for comment in comments:
		if comment.parent_comment_id != None:
			if comment.parent_comment_id not in newdict:
				newdict[comment.parent_comment_id] = [comment]
			else:
				newdict[comment.parent_comment_id].append(comment)

	# how you access the database

	return render_template("viewpost.html", post=post, path=subforum.path, comments=comments, newdict = newdict)

# Route to get all private messages for current user
@login_required
@app.route('/get_messages_for_user')
def get_messages_for_user():	
	messages = DirectMessage.query.filter_by(receiver_id=current_user.id)
	senders = get_sending_usernames(messages)
	return render_template('usermessages.html', messages=messages, senders=senders)

@login_required
@app.route('/createmessage')
def createmessage():
	return render_template('createmessage.html')

def get_sending_usernames(msgs):
	'''
	Returns a dict of: {key: sender_id, value: sender_username}
	'''
	sending_usernames = {}
	for msg in msgs:
		user = User.query.filter_by(id=msg.sender_id).first()
		if msg.sender_id not in sending_usernames:
			sending_usernames[msg.sender_id] = user.username
	return sending_usernames

#ACTIONS

@login_required
@app.route('/action_comment', methods=['POST', 'GET'])
# '/action_comment' is how viewpost.html calls comment()
def comment():
	post_id = int(request.args.get("post")) # goes to the post table and gets the post_id
	# .args.get("post") is from viewpost.html
	# ?post = {{post.id}}

	post = Post.query.filter(Post.id == post_id).first() # checks to make sure post id exists and returns the first 
	# a query is a select statement

	if not post:
		return error("That post does not exist!")
	content = request.form['content']

	
	
	# replaces key word with emoji
	if '*wink*' in content:
		content = content.replace('*wink*', '\U0001F609')
	if '*smile*' in content:
		content = content.replace('*smile*', '\U0001F600')
	if '*like*' in content:
		content = content.replace('*like*', '\U0001F44D')
	if '*spooky*' in content:
		content = content.replace('*spooky*', '\U0001F47B')


	postdate = datetime.datetime.now()
	comment = Comment(content, postdate, current_user.id, post_id)
	# this creates an instance of comment
	db.session.add(comment)
	db.session.commit()
	return redirect("/viewpost?post=" + str(post_id))


# create a route that sets passes a ?id= {{comment.id}} method = 'POST'
# grab parent comment id with int(request.args.get(comment.id))
# make sure route name is unique
# 1) make sure you're getting all data in form 
# 2) putting data into the database

@login_required
@app.route('/comment_comment', methods = ['POST', 'GET'])
# '/action_comment' is how viewpost.html calls comment()
def comment_comment():
	post_id = int(request.args.get("post")) 
	post = Post.query.filter(Post.id == post_id).first() 

	parent_id = int(request.args.get("parent"))
	print(parent_id)
	parent = Comment.query.filter(Comment.id == parent_id).first()
	if not post:
		return error("That post does not exist!")
	content = request.form['content']

	if not parent:
		return error("This parent comment does not exist!")
	
	# Like button
	like_counter = 0
	if request.method == 'POST':
		if request.form.get('action1') == 'Like':
			print('hello')
	
	
	# replaces key word with emoji
	if '*wink*' in content:
		content = content.replace('*wink*', '\U0001F609')
	if '*smile*' in content:
		content = content.replace('*smile*', '\U0001F600')
	if '*like*' in content:
		content = content.replace('*like*', '\U0001F44D')


	postdate = datetime.datetime.now()

	#  content, postdate, user_id, post_id, parent_comment_id = None
	comment = Comment(content, postdate, current_user.id, post_id, parent_comment_id = parent_id)
	# this creates an instance of comment
	#go to the post table, go to the comments column, and then add the comment

	db.session.add(comment)
	db.session.commit()
	return redirect("/viewpost?post=" + str(post_id))

@login_required
@app.route('/action_post', methods=['POST'])
def action_post():
	subforum_id = int(request.args.get("sub"))
	subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
	if not subforum:
		return redirect(url_for("subforums"))

	user = current_user
	title = request.form['title']
	content = request.form['content']
	private = request.form['private']

	# replaces key word with emoji
	if '*wink*' in content or '*wink*' in title:
		content = content.replace('*wink*', '\U0001F609')
		title = title.replace('*wink*', '\U0001F609')
	if '*smile*' in content or '*smile*' in title:
		content = content.replace('*smile*', '\U0001F600')
		title = title.replace('*smile*', '\U0001F600')
	if '*like*' in content or '*like*' in title:
		content = content.replace('*like*', '\U0001F44D')
		title = title.replace('*like*', '\U0001F44D')
	if '*spooky*' in content or '*spooky*' in title:
		content = content.replace('*spooky*', '\U0001F47B')
		title = title.replace('*spooky*', '\U0001F47B')
	


	#check for valid posting
	errors = []
	retry = False
	if not valid_title(title):
		errors.append("Title must be between 4 and 140 characters long!")
		retry = True
	if not valid_content(content):
		errors.append("Post must be between 10 and 5000 characters long!")
		retry = True
	if retry:
		return render_template("createpost.html",subforum=subforum,  errors=errors)
	post = Post(title, content,datetime.datetime.now()) #this is where post are set to public or private'''
	subforum.posts.append(post)
	user.posts.append(post)
	db.session.commit()
	return redirect("/viewpost?post=" + str(post.id))



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


# Action to send a message
@login_required
@app.route('/action_sendmessage', methods=['POST'])
def action_sendmessage():
	errors = []
	receiver_username = request.form['username']
	message_body = request.form['message_body']
	# check is user exists
	user = User.query.filter_by(username=receiver_username).first()
	if user is None:
		errors.append('User does not exist')
		return render_template('createmessage.html', errors=errors)
	# check if message is empty
	if len(message_body) == 0:
		errors.append('Cannot send empty message')
		return render_template('createmessage.html', errors=errors)
	# create new message and commit to database
	new_message = DirectMessage(current_user.id, user.id, message_body)
	db.session.add(new_message)
	db.session.commit()
	return render_template('messagesentsuccess.html')

#Chuck stuff start
@login_required
@app.route('/action_changeusername', methods=['POST'])
def action_changeusername():
	
	id1 = current_user.id
	new_username = request.form['username']
	errors = []
	retry = False
	if username_taken(new_username):
		errors.append("Username is already taken!")
		retry=True
	if not valid_username(new_username):
		errors.append("Username is not valid!")
		retry = True
	if retry:
		return render_template("userinfo.html", errors=errors)
	
	db.session.query(User).filter(User.id == id1).update({"username": new_username}, synchronize_session="fetch")
	db.session.commit()
	
	return redirect('/userinfo')

@login_required
@app.route('/action_changeemail', methods=['POST'])
def action_changeemail():
	
	id1 = current_user.id
	new_email = request.form['email']
	errors = []
	retry = False
	if email_taken(new_email):
		errors.append("Email is already taken!")
		retry=True
	if retry:
		return render_template("userinfo.html", errors=errors)
	
	db.session.query(User).filter(User.id == id1).update({"email": new_email}, synchronize_session="fetch")
	db.session.commit()
	
	return redirect('/userinfo')

@login_required
@app.route('/action_changepassword', methods=['POST'])
def action_changepassword():
	
	id1 = current_user.id
	'''
	errors = []
	retry = False
	input_current_password = request.form['current_password']
	unhashed_password = User.query.filter(User.password_hash == id1)
	input_current_password_hashed = generate_password_hash(input_current_password)
	if input_current_password_hashed != unhashed_password:
		errors.append("Incorrect current password!")
		retry=True
	if retry:
		return render_template("userinfo.html", errors=errors)
	'''
	new_password = request.form['new_password']
	new_password_hash = generate_password_hash(new_password)
	db.session.query(User).filter(User.id == id1).update({"password_hash": new_password_hash}, synchronize_session="fetch")
	db.session.commit()
	
	return redirect('/userinfo')
#chuck stuff end

def error(errormessage):
	return "<b style=\"color: red;\">" + errormessage + "</b>"

def generateLinkPath(subforumid):
	links = []
	subforum = Subforum.query.filter(Subforum.id == subforumid).first()
	parent = Subforum.query.filter(Subforum.id == subforum.parent_id).first()
	links.append("<a href=\"/subforum?sub=" + str(subforum.id) + "\">" + subforum.title + "</a>")
	while parent is not None:
		links.append("<a href=\"/subforum?sub=" + str(parent.id) + "\">" + parent.title + "</a>")
		parent = Subforum.query.filter(Subforum.id == parent.parent_id).first()
	links.append("<a href=\"/\">Forum Index</a>")
	link = ""
	for l in reversed(links):
		link = link + " / " + l
	return link


#from forum.app import db, app 


login_manager = LoginManager()
login_manager.init_app(app)

# if __name__ == "__main__":
# 	#runsetup()
# 	port = int(os.environ["PORT"])
# 	app.run(host='0.0.0.0', port=port, debug=True)



#DATABASE STUFF
@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)


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


#OBJECT MODELS
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, unique=True)
	password_hash = db.Column(db.Text)
	email = db.Column(db.Text, unique=True)
	admin = db.Column(db.Boolean, default=False, unique=True)
	posts = db.relationship("Post", backref="user")
	comments = db.relationship("Comment", backref="user")

	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	content = db.Column(db.Text)
	comments = db.relationship("Comment", backref="post")
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	subforum_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
	postdate = db.Column(db.DateTime)
	privatepost = db.Column(db.Boolean, default=False)

	#cache stuff
	lastcheck = None
	savedresponce = None
	def __init__(self, title, content, postdate):
		self.title = title
		self.content = content
		self.postdate = postdate
		#self.privatepost = privatepost
	def get_time_string(self):
		#this only needs to be calculated every so often, not for every request
		#this can be a rudamentary chache
		now = datetime.datetime.now()
		if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
			self.lastcheck = now
		else:
			return self.savedresponce

		diff = now - self.postdate

		seconds = diff.total_seconds()
		print(seconds)
		if seconds / (60 * 60 * 24 * 30) > 1:
			self.savedresponce =  " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
		elif seconds / (60 * 60 * 24) > 1:
			self.savedresponce =  " " + str(int(seconds / (60*  60 * 24))) + " days ago"
		elif seconds / (60 * 60) > 1:
			self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
		elif seconds / (60) > 1:
			self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
		else:
			self.savedresponce =  "Just a moment ago!"

		return self.savedresponce

# a 'Subforum' model is a table, and all the models make up the database
# a model's attributes are its columns when defined with db.Column

# so below we have the subforum model
# the order is id, title, description, parent_id
# id is the primary key
# title, description are columns
# parent_id sets subforum.id as the parent key
# subforums has a r


class Subforum(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text, unique=True)
	description = db.Column(db.Text)
	subforums = db.relationship("Subforum")
	parent_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
	posts = db.relationship("Post", backref="subforum") # Post's table is going to get a virtual column of subforum
	path = None
	hidden = db.Column(db.Boolean, default=False)
	def __init__(self, title, description):
		self.title = title
		self.description = description

#wes work 

'''class Subforum_2(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text, unique=True)
	description = db.Column(db.Text)
	subforums = db.relationship("Subforum")
	parent_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
	posts = db.relationship("Post", backref="subforum") # Post's table is going to get a virtual column of subforum
	path = None
	hidden = db.Column(db.Boolean, default=False)
	def __init__(self, title, description):
		self.title = title
		self.description = description'''
#wes work end

# order is id, content, postdate, user_id, post_id
# we set parent_comment_id as the hcild key, id as the parent_key 

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)              # every comment gets a primary key
	content = db.Column(db.Text) 							  # body
	postdate = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case looks at a table, upper case looks at a class
	post_id = db.Column(db.Integer, db.ForeignKey("post.id")) # parent article
	
	comments = db.relationship("Comment") # relates to 
	parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), default = None)

	lastcheck = None
	savedresponce = None
	def __init__(self, content, postdate, user_id, post_id, parent_comment_id = None):
		self.content = content
		self.postdate = postdate
		self.user_id = user_id
		self.post_id = post_id
		self.parent_comment_id = parent_comment_id




	def get_time_string(self):
		#this only needs to be calculated every so often, not for every request
		#this can be a rudamentary chache
		now = datetime.datetime.now()
		if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
			self.lastcheck = now
		else:
			return self.savedresponce

		diff = now - self.postdate
		seconds = diff.total_seconds()
		if seconds / (60 * 60 * 24 * 30) > 1:
			self.savedresponce =  " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
		elif seconds / (60 * 60 * 24) > 1:
			self.savedresponce =  " " + str(int(seconds / (60*  60 * 24))) + " days ago"
		elif seconds / (60 * 60) > 1:
			self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
		elif seconds / (60) > 1:
			self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
		else:
			self.savedresponce =  "Just a moment ago!"
		return self.savedresponce


# AIDAN WAS HERE
class DirectMessage(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer)
	receiver_id = db.Column(db.Integer)
	body = db.Column(db.String(256))  # limit 256 chars in message

	def __init__(self, sender_id, receiver_id, body):
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		self.body = body


def init_site():
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
"""
def interpret_site_value(subforumstr):
	segments = subforumstr.split(':')
	identifier = segments[0]
	description = segments[1]
	parents = []
	hasparents = False
	while('.' in identifier):
		hasparents = True
		dotindex = identifier.index('.')
		parents.append(identifier[0:dotindex])
		identifier = identifier[dotindex + 1:]
	if hasparents:
		directparent = subforum_from_parent_array(parents)
		if directparent is None:
			print(identifier + " could not find parents")
		else:
			add_subforum(identifier, description, directparent)
	else:
		add_subforum(identifier, description)

def subforum_from_parent_array(parents):
	subforums = Subforum.query.filter(Subforum.parent_id == None).all()
	top_parent = parents[0]
	parents = parents[1::]
	for subforum in subforums:
		if subforum.title == top_parent:
			cur = subforum
			for parent in parents:
				for child in subforum.subforums:
					if child.title == parent:
						cur = child
			return cur
	return None


def setup():
	siteconfig = open('./config/subforums', 'r')
	for value in siteconfig:
		interpret_site_value(value)
"""
#db.drop_all()

db.create_all()
if not Subforum.query.all():
		init_site()

