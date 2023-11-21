from flask import *
from forum.forum import db, app
from forum.post import Post
from forum.app import error


class Subforum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    subforums = db.relationship("Subforum")
    parent_id = db.Column(db.Integer, db.ForeignKey('subforum.id'))
    posts = db.relationship("Post", backref="subforum")
    path = None
    hidden = db.Column(db.Boolean, default=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

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

@app.route('/')
def index():
    subforums = Subforum.query.filter(Subforum.parent_id == None).order_by(Subforum.id)
    return render_template("subforums.html", subforums=subforums)


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

def init_site():
    admin = add_subforum("Forum", "Announcements, bug reports, and general discussion about the forum belongs here")
    add_subforum("Announcements", "View forum announcements here",admin)
    add_subforum("Bug Reports", "Report bugs with the forum here", admin)
    add_subforum("General Discussion", "Use this subforum to post anything you want")
    add_subforum("Other", "Discuss other things here")

# db.drop_all()
db.create_all()
if not Subforum.query.all():
    init_site()
