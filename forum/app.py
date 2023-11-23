from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# from forum.post import post_views

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY=b'kristofer',
    SITE_NAME="Schooner",
    SITE_DESCRIPTION="a schooner forum",
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/database.db',
    DEBUG=True
)

import os

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    print("setting db url for postgres")
else:
    print("DATABASE_URL is not set, using sqlite")

db = SQLAlchemy(app)

# def error(errormessage):
# 	return "<b style=\"color: red;\">" + errormessage + "</b>"


login_manager = LoginManager()
login_manager.init_app(app)

# post_views(app)
