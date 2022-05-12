import time
from flask_sock import Sock
from os import listdir
from os.path import isfile, join
import random
import json
from typing import List

import authentication
from message import handle_chat, get_chat, get_all_pfps, receive_notification, send_list_msg, fix_list_msg
import database
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from authentication import handle_login, get_login_page, get_username, handle_logout
import avatar
from pong import pongapi
from pong.pong_views import handle_game_page_request
from pong.pongapi import find_current_game, clean_up_idle_games
import food.achievement_database

app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # limits uploaded profile image size to 16MB
sock = Sock(app)
database.initialize()


# NOTE: Please try to keep this file as clean as possible! redirect to other python files to do the actual logic

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


# method gets images, CSS, and JS
@app.route("/static/<path:filename>", methods=['GET'])
def static(filename):
    resp = send_from_directory("static", filename)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


@app.route("/about", methods=['GET'])
def request_about():
    data = {"all_users": authentication.get_all_logged_in_users(), "len": len(authentication.get_all_logged_in_users())}

    number_random_ingredients = 5
    path: str = "./static/ingredients/"
    ingredient_files: List[str] = [join(path, file) for file in listdir(path) if isfile(join(path, file))]
    sample: List[str] = random.sample(ingredient_files, number_random_ingredients)
    # data: Dict[str, str] = {}
    for i in range(0, number_random_ingredients):
        data["ingred" + str(i + 1) + "_src"] = sample[i]

    return render_template("div_templates/about.html", **data)


@app.route("/about_ingredients", methods=['GET'])
def get_about_ingredients():
    number_random_ingredients = 5
    path: str = "./static/ingredients/"
    ingredient_files: List[str] = [join(path, file) for file in listdir(path) if isfile(join(path, file))]
    sample: List[str] = random.sample(ingredient_files, number_random_ingredients)
    return json.dumps(sample)


# get the messages with the other user
@app.route("/messages/<username>", methods=['GET'])
def request_message_user(username: str):
    main_user = get_username(request)
    s = fix_list_msg(username, main_user)
    get_data = get_chat(main_user, username)
    all_users_pfps = get_all_pfps(authentication.get_all_logged_in_users())
    data = {"user": username, "main_user": main_user, "chat_list": get_data, "all_user_pfps": all_users_pfps,
            "len_chat": len(get_data), "all_users": authentication.get_all_logged_in_users(),
            "len": len(authentication.get_all_logged_in_users())}
    return render_template("div_templates/message.html", **data)


# store the message into the database
@app.route("/messages/<username>", methods=['POST'])
def post_message(username: str):
    msg = request.get_json(force=True)
    main_user = get_username(request)
    all_users_pfps = get_all_pfps(authentication.get_all_logged_in_users())
    get_data = handle_chat(msg, main_user, username)
    data = {"user": username, "main_user": main_user, "chat_list": get_data, "all_user_pfps": all_users_pfps,
            "len_chat": len(get_data), "all_users": authentication.get_all_logged_in_users(),
            "len": len(authentication.get_all_logged_in_users())}
    s = receive_notification(username, main_user)
    return render_template("div_templates/message.html", **data)


# handle the new message notifications
@app.route("/newmessage", methods=['GET'])
def request_newmessage():
    data = []
    username = get_username(request)
    list_msg = send_list_msg()
    for one_msg in list_msg:
        if (one_msg[1] == username):  # get the msg that was sent to_user
            data.append([one_msg[0], username])
    main_data = {"list_of_notifications": data}
    return render_template("notification_template/notification.html", **main_data)


@app.route("/messages/<username>", methods=['GET'])
def request_message(username: str):
    main_user = get_username(request)
    get_data = get_chat(main_user, username)
    all_users_pfps = get_all_pfps(authentication.get_all_logged_in_users())
    data = {"user": username, "main_user": main_user, "chat_list": get_data, "all_user_pfps": all_users_pfps,
            "len_chat": len(get_data), "all_users": authentication.get_all_logged_in_users(),
            "len": len(authentication.get_all_logged_in_users())}
    # data = {"user": username, "sent_msg": "","main_user": get_username(request), "all_users": authentication.get_all_logged_in_users(),"len": len(authentication.get_all_logged_in_users())}
    return render_template("div_templates/message.html", **data)


# @app.route("/messages/<username>", methods=['POST'])
# def post_message(username: str):
#     msg = request.get_json(force=True)
#     main_user = get_username(request)
#     all_users_pfps = get_all_pfps(authentication.get_all_logged_in_users())
#     get_data = handle_chat(msg, main_user, username)
#     data = {"user": username, "main_user": main_user, "chat_list": get_data, "all_user_pfps": all_users_pfps, "len_chat": len(get_data), "all_users": authentication.get_all_logged_in_users(), "len": len(authentication.get_all_logged_in_users())}
#     # data = {"user": username, "sent_msg": msg, "main_user": main_user, "all_users": authentication.get_all_logged_in_users(),"len": len(authentication.get_all_logged_in_users())}
#     return render_template("div_templates/message.html", **data)


@app.route("/contact", methods=['GET'])
def request_contact():
    return render_template("div_templates/contact.html")


@app.route("/profile", methods=['GET'])
def request_profile():
    user = get_username(request)
    profile = database.user_profiles.find_one({'username': user})
    achievements = food.achievement_database.get_player_achievements(user)
    to_send = {}
    if profile != None:
        to_send = {"pfp": profile["pfp"], "username": user, "achievements": achievements}
    return render_template("div_templates/profile.html", **to_send)


@app.errorhandler(413)
def pfp_too_big(e):
    user = get_username(request)
    profile = database.user_profiles.find_one({'username': user})
    achievements = food.achievement_database.get_player_achievements(user)
    to_send = {"pfp": profile["pfp"], "username": user,
               "error": "WOAH! This file exceeds the size of our universe. Please choose something smaller.",
               "achievements": achievements}
    return render_template("div_templates/profile.html", **to_send)


@app.route("/homepage", methods=['GET'])
def request_homepage():
    username = get_username(request)
    all_users_pfps = get_all_pfps(authentication.get_all_logged_in_users())
    data = {"username": username, "main_user": username, "all_users": authentication.get_all_logged_in_users(),
            "all_user_pfps": all_users_pfps}
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


# Handle clicking the logout EVERYWHERE button
@app.route("/auth/logout-everywhere", methods=['POST'])
def request_logout_everywhere():
    return handle_logout(request, all_sessions=True)


@app.route("/change_avatar", methods=['POST'])
def change_avatar():
    return avatar.change_avatar(request, database.user_profiles, get_username(request))


@app.route("/default_avatar", methods=['POST'])
def default_avatar():
    return avatar.default_avatar(database.user_profiles, get_username(request))


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
    # print("Websocket connection username: " + username)
    while game.game_thread_running and socket.connected:
        raw_data = socket.receive(timeout=0)
        if raw_data:
            game.on_websocket_message(username, raw_data)
        data_to_send: str = json.dumps(game.to_all_clients())
        socket.send(data_to_send)
        time.sleep(1 / game.config.framerate)


# @app.route("/create_game_testing", methods=['GET'])
# def create_game_testing():
#     my_cool_config = PongConfig()
#     my_cool_config.framerate = 300
#     game = create_new_game(config=my_cool_config)
#     return f"Game created: {game.uid}", 201


@app.route("/games", methods=['GET'])
def games():
    data = {
        "current_games": pongapi.get_current_games(),
        "recent_games": pongapi.get_recent_games(),
    }
    return render_template("pong_templates/games.html", **data)


@app.route("/cleanup-games", methods=['GET'])
def cleanup_games():
    clean_up_idle_games()
    return redirect(url_for("games"), code=302)


if __name__ == "__main__":
    app.run("0.0.0.0", 9091)
