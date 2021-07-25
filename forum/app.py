from flask import Flask

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY=b'kristofer',
	SITE_NAME = "DataFam",
	SITE_DESCRIPTION = "a non-Java forum for only the most 1337 Python hackers",
	SQLALCHEMY_DATABASE_URI='sqlite:////tmp/database.db' #relative pass to physical db location (this has 4 /)
)


