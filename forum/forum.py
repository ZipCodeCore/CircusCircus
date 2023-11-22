
import re
from flask import current_app
from flask_login import current_user
import datetime

from flask_login.utils import login_required

import datetime

from flask import render_template, request, redirect, url_for
from forum.utils import valid_content, valid_title
from .models import db, Subforum, User, Post, Comment
# adding db url


#VIEWS
