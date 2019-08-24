"""Using Flask as the framework to generate a site that displays date time
Code based on CS50 2019 Week 7 Shorts

To run the file in terminal:
export FLASK_APP=display_datetime.py
export FLASK_DEBUG=1
flask run
"""
from flask import Flask
from datetime import datetime
from pytz import timezone

# initialise flask application
app = Flask(__name__)

# the following is decorator in Flask to associate a particular function with a particular URL
@app.route("/")

def time():
    now = datetime.now(timezone('Australia/Sydney'))
    return "The current date and time in Sydney is {}".format(now)

# def index():
#     return "You are on the index page"

# @app.route("/sample")
# def sample():
#     return "You are on the sample page"


