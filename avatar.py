import random
from werkzeug.utils import secure_filename #for profile image uploads
from flask import render_template
import secrets

def sign_up(username, user_profiles):
    random_init = random.randint(1,8)
    user_profiles.insert_one({'username': username, 'pfp': 'static/avatar'+str(random_init)+'.jpg'})

def change_avatar(request, user_profiles, username):
    up = request.files['upload']
    secured = secure_filename(up.filename)
    up.save(secured)
    image_to_be = "./static/avatar"+secrets.token_urlsafe(20)
    with open(secured, "rb") as f:
        with open(image_to_be,"wb") as f2:
            for byte in f:
                f2.write(byte)
    new_pic = {"$set": {"pfp": image_to_be}}
    user_profiles.update_one({"username": username}, new_pic)
    profile = user_profiles.find_one({'username': username})
    to_send = {"pfp":profile["pfp"], "username": username}
    return render_template("div_templates/profile.html", **to_send)