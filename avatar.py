import random
from werkzeug.utils import secure_filename #for profile image uploads
from flask import render_template
import secrets
import food.achievement_database

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif','ico'}

def sign_up(username, user_profiles):
    random_init = random.randint(1,8)
    user_profiles.insert_one({'username': username, 'pfp': 'static/avatars/avatar'+str(random_init)+'.jpg'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions #from https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/ to check if it is an image file we want

def change_avatar(request, user_profiles, username):
    up = request.files['upload']
    to_send = {}
    if up and allowed_file(up.filename):
        secured = secure_filename("static/avatars/"+up.filename)
        up.save(secured)
        image_to_be = "static/avatars/avatar"+secrets.token_urlsafe(20)+"."+up.filename.rsplit('.', 1)[1].lower()
        with open(secured, "rb") as f:
            with open(image_to_be,"wb") as f2:
                for byte in f:
                    f2.write(byte)
        new_pic = {"$set": {"pfp": image_to_be}}
        user_profiles.update_one({"username": username}, new_pic)
    elif not up:
        to_send["error"]="You need to upload a file to send to the stars!"
    else:
        to_send["error"] ="The Pulsar Council does not accept that type of file for a profile picture."
    profile = user_profiles.find_one({'username': username})
    to_send["pfp"]=profile["pfp"]
    to_send["username"]=username
    achievements = food.achievement_database.get_player_achievements(username)
    to_send["achievements"] = achievements
    return render_template("div_templates/profile.html", **to_send)

def default_avatar(user_profiles, username):
    to_send = {}
    random_init = random.randint(1,8)
    new_pic = {"$set": {"pfp": 'static/avatars/avatar'+str(random_init)+'.jpg'}}
    user_profiles.update_one({'username': username}, new_pic)
    profile = user_profiles.find_one({'username': username})
    to_send["pfp"]=profile["pfp"]
    to_send["username"]=username
    achievements = food.achievement_database.get_player_achievements(username)
    to_send["achievements"] = achievements
    return render_template("div_templates/profile.html", **to_send)