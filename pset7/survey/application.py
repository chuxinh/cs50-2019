import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

def check_missing_values(missing_field_list, field, field_description):
    if not field:
        missing_field_list.append(field_description)
    return missing_field_list

@app.route("/form", methods=["POST"])
def post_form():
    missing_fields = []

    name = request.form.get("name")
    missing_fields = check_missing_values(missing_fields, name, "name")

    house = request.form.get("house")
    missing_fields = check_missing_values(missing_fields, house, "house")

    role = request.form.get("role")
    missing_fields = check_missing_values(missing_fields, role, "role")

    if missing_fields:

        message = print("Missing " + ', '.join(missing_fields))
        return render_template("error.html", message = message)

    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((name, house, role))

    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        table = list(reader)
    return render_template("sheet.html", table=table)
