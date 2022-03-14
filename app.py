import os

import pymongo
from flask import Flask, send_from_directory, render_template, request
import do_request

app = Flask(__name__)

# Create database collections here, and pass as parameter
client = pymongo.MongoClient(os.getenv("MONGO_HOST", "localhost"))
db = client.mydata
users = db.users  # creating/retrieving a collection for saving usernames and passwords
count_users = db.count_users  # creating/retrieving a collection for saving the amount of users we have


# NOTE: Please try to keep this file as clean as possible! redirect to other python files to do the actual logic

@app.route("/", methods=['GET'])
def index():
    data = {"food": "Pizza"}
    return render_template("index.html", **data)


# method gets images, CSS, and JS
@app.route("/static/<path:file>", methods=['GET'])
def static_files(file):
    return send_from_directory("static", file)


# method to sign a user in
@app.route("/sign-in", methods=['POST'])
def request_sign_in():
    return do_request.sign_in(request, users, count_users)


if __name__ == "__main__":
    app.run("0.0.0.0", 9091)
