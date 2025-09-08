#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response
import random
from urllib.parse import quote_plus
from pathlib import Path
import json

app = Flask(__name__)


@app.route("/")
def index():

    # You'll need to pull data from the database.  Here were just 
    # hard coding a dataset, but the principle is the same
    data = [
        {"name":"Simon", "value":10},
        {"name": "Bob", "value": 20},
        {"name": "Alice", "value": 30}
    ]

    return render_template("index.html", data=data)


def get_form():
    # In addition to the main arguments we also add the session
    # string from the cookie
    session = ""

    if "groupactivity_session_id" in request.cookies:
        session = request.cookies["groupactivity_session_id"]

    if request.method == "GET":
        form = request.args.to_dict(flat=True)
        form["session"] = session
        return form

    elif request.method == "POST":
        form = request.form.to_dict(flat=True)
        form["session"] = session
        return form



