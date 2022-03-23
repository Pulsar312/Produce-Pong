import database
from flask import Flask, send_from_directory, render_template, request
import do_request
from authentication import handle_login, get_login_page, get_username, handle_logout

app = Flask(__name__)
database.initialize()

# NOTE: Please try to keep this file as clean as possible! redirect to other python files to do the actual logic

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


# method gets images, CSS, and JS
@app.route("/static/<path:file>", methods=['GET'])
def static_files(file):
    return send_from_directory("static", file)


@app.route("/about", methods=['GET'])
def request_about():
    data = {"dessert": "ice cream", "ingredients": ["cream", "sugar", "sprinkles"]}
    return render_template("div_templates/about.html", **data)


@app.route("/contact", methods=['GET'])
def request_contact():
    return render_template("div_templates/contact.html")

  
@app.route("/profile", methods=['GET'])
def request_profile():
    user = get_username(request)
    profile = database.user_profiles.find_one({'username': user})
    toSend ={}
    if profile != None:
        toSend = {"pfp": profile["pfp"],"username": user}
    return render_template("div_templates/profile.html", **toSend)


@app.route("/homepage", methods=['GET'])
def request_homepage():
    username = get_username(request)
    data = {"username": username}
    return render_template("div_templates/homepage.html", **data)


@app.route("/header", methods=['GET'])
def request_header():
    data = {"logged_in": get_username(request)}
    return render_template("header_templates/header.html", **data)


# Get the login page
@app.route("/play", methods=['GET'])
def request_play():
    return get_login_page()


# Handle the login form being submitted through Ajax
@app.route("/auth/login", methods=['POST'])
def request_login():
    return handle_login(request)


# Handle clicking the logout button
@app.route("/auth/logout", methods=['POST'])
def request_logout():
    return handle_logout(request)


@app.route("/change_avatar", methods=['POST'])
def change_avatar():
    return do_request.change_avatar(request, database.user_profiles, get_username(request))



if __name__ == "__main__":
    app.run("0.0.0.0", 9091)
