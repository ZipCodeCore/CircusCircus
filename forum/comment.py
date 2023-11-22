import datetime
from forum.app import app, db, error
from forum.model import *

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text)
#     postdate = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
#
#     lastcheck = None
#     savedresponce = None
#
#     def __init__(self, content, postdate):
#         self.content = content
#         self.postdate = postdate
#
#     def get_time_string(self):
#         # this only needs to be calculated every so often, not for every request
#         # this can be a rudamentary chache
#         now = datetime.datetime.now()
#         if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
#             self.lastcheck = now
#         else:
#             return self.savedresponce
#
#         diff = now - self.postdate
#         seconds = diff.total_seconds()
#         if seconds / (60 * 60 * 24 * 30) > 1:
#             self.savedresponce = " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
#         elif seconds / (60 * 60 * 24) > 1:
#             self.savedresponce = " " + str(int(seconds / (60 * 60 * 24))) + " days ago"
#         elif seconds / (60 * 60) > 1:
#             self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
#         elif seconds / (60) > 1:
#             self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
#         else:
#             self.savedresponce = "Just a moment ago!"
#         return self.savedresponce


# @login_required
# @app.route('/action_comment', methods=['POST', 'GET'])
# def comment():
#
#     post_id = int(request.args.get("post"))
#     post = Post.query.filter(Post.id == post_id).first()
#     if not post:
#         return error("That post does not exist!")
#     content = request.form['content']
#     postdate = datetime.datetime.now()
#     comment = Comment(content, postdate)
#     current_user.comments.append(comment)
#     post.comments.append(comment)
#     db.session.commit()
#     return redirect("/viewpost?post=" + str(post_id))
#

