"""Data can be passed via URLs, akin to using HTTP GET
"""
from flask import Flask
from datetime import datetime
from pytz import timezone

@app.route("show/<number>")
def show(number):
    return "Your passed in {}".format(number)