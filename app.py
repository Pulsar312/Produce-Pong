import database
from flask import Flask, send_from_directory, render_template, request
import do_request
from authentication import handle_login, get_login_page, get_username

app = Flask(__name__)
database.initialize()


# NOTE: Please try to keep this file as clean as possible! redirect to other python files to do the actual logic

@app.route("/", methods=['GET'])
def index():
    data = {"food": "Pizza"}
    return render_template("index.html", **data)


# method gets images, CSS, and JS
@app.route("/static/<path:file>", methods=['GET'])
def static_files(file):
    return send_from_directory("static", file)


@app.route("/about", methods=['GET'])
def request_about():
    return render_template("div_templates/about.html")


@app.route("/contact", methods=['GET'])
def request_contact():
    return render_template("div_templates/contact.html")


@app.route("/profile", methods=['GET'])
def request_profile():
    return render_template("div_templates/profile.html")


@app.route("/homepage", methods=['GET'])
def request_homepage():
    username = get_username(request)
    data = {"username": username}
    return render_template("div_templates/homepage_templates/homepage-signed-in.html", **data)
    # return do_request.homepage(request)


@app.route("/header", methods=['GET'])
def request_header():
    data = {"logged_in": get_username(request)}
    return render_template("header_templates/header.html", **data)


# method to sign a user in
# @app.route("/sign-in", methods=['POST'])
# def request_sign_in():
#     return do_request.sign_in(request, users, count_users)

# Get the login page
@app.route("/play", methods=['GET'])
def request_play():
    return get_login_page()


# Handle the login form being submitted through Ajax
@app.route("/auth/login", methods=['POST'])
def request_login():
    return handle_login(request)


if __name__ == "__main__":
    app.run("0.0.0.0", 9091)
