import pymongo
from flask import Flask, send_from_directory, render_template

app = Flask(__name__)


client = pymongo.MongoClient('mongo')
db = client.mydata

@app.route("/")
def index():
    data = {"food": "Pizza"}
    return render_template("index.html", **data)


@app.route("/static/<path:file>")
def static_files(file):
    return send_from_directory("static", file)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
