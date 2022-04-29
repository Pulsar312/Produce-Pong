import json
import time
from flask_sock import Sock
import database
from flask import Flask, send_from_directory, render_template, request
from authentication import handle_login, get_login_page, get_username, handle_logout
import avatar
from food.Recipe import Recipe
from food.chef import Chef
from pong.PongConfig import PongConfig
from pong.pong_views import handle_game_page_request
from pong.pongapi import create_new_game, find_current_game

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # limits uploaded profile image size to 16MB
sock = Sock(app)
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
    to_send = {}
    if profile != None:
        to_send = {"pfp": profile["pfp"], "username": user}
    return render_template("div_templates/profile.html", **to_send)


@app.errorhandler(413)
def pfp_too_big(e):
    user = get_username(request)
    profile = database.user_profiles.find_one({'username': user})
    to_send = {"pfp": profile["pfp"], "username": user, "error": "WOAH! This file exceeds the size of our universe. Please choose something smaller."}
    return render_template("div_templates/profile.html", **to_send)


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
    return avatar.change_avatar(request, database.user_profiles, get_username(request))


@app.route("/game/<game_id>", methods=['GET'])
def request_game(game_id: str):
    return handle_game_page_request(request, game_id)


@sock.route("/gamews/<game_id>")
def request_game_websocket(socket, game_id: str):
    username = get_username(request)
    if not username:
        return
    game = find_current_game(game_id)
    if not game:
        return
    print("Websocket connection username: " + username)
    while True:
        # TODO exit this loop once the websocket connection closes
        # Maybe while socket.connected:
        raw_data = socket.receive(timeout=0)
        if raw_data:
            game.on_websocket_message(username, raw_data)
        socket.send(json.dumps(game.to_all_clients()))
        time.sleep(1 / game.config.framerate)


@app.route("/create_game_testing", methods=['GET'])
def create_game_testing():
    my_cool_config = PongConfig()
    my_cool_config.framerate = 300
    game = create_new_game(config=my_cool_config)
    return f"Game created: {game.uid}", 201


@app.route("/default_avatar", methods=['POST'])
def default_avatar():
    return avatar.default_avatar(database.user_profiles, get_username(request))


if __name__ == "__main__":
    app.run("0.0.0.0", 9091)
