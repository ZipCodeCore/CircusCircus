from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# from forum.post import post_views

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY=b'kristofer',
	SITE_NAME = "Spoon O Fork",
	SITE_DESCRIPTION = "a spooner forum",
	SQLALCHEMY_DATABASE_URI='sqlite:////tmp/database.db',
	DEBUG=True,
	FLASK_DEBUG=1,
	FOOTER_SIGNATURE = "some spoon",
	COPYRIGHT = "©Copyright: All rights reserved. No part of this forum may be reproduced in any form or by any electronic "
				" or mechanical means, including information storage and retrival systems, without permission in"
				" writing from the publisher, except owner of the forum.\n",
	NEW_LINE = "\n",
	ABOUT_SITE = "The Spooner Forum first began on November 21, 2023. It was started by four data students of Zip Code"
				 "\nWilmington. This tasked was imposed on them by their fearless leader, Instructor Kris. It was demanded"
				 "of them to be finished with a week, with whatever theme they chose of. They decided to do a forum on"
				 "spoons. Specifically, a forum about which utensil is better; spoons or forks. This is a battle that will"
				 "go down in history! Stay tuned to see which utensil will conquer! This is a job for the only data students",
	SPOON = "Spoon",
	FORK = "Fork"
)

import os
if os.getenv("DATABASE_URL"):
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
	print("setting db url for postgres")
else:
	print("DATABASE_URL is not set, using sqlite")

db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)

# post_views(app)