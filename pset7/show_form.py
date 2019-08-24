"""Data can be passed via HTML forms, as with HTTP POST,
but we need to direct Flask to respond to HTTP POST.
Default is HTTP GET
"""
from flask import Flask
from datetime import datetime
from pytz import timezone

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if not request.form.get("username")
        return apology("must provider username")