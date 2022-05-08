import json
import time
from flask_sock import Sock

import authentication
import database
from flask import Flask, send_from_directory, render_template, request


# ------------messages handling methods ----------------#
# {"from": user1, "to": user2, "message": message_sent}


# gets the msg from the user, inserts it into the database,
# and returns all the chat history between two people
def handle_chat(msg: str, main_user: str, username: str):
    parse_message=json.loads(json.dumps(msg))
    parse_message_data=parse_message["send_msg"]
    data = {"from": main_user, "to": username, "message": parse_message_data}
    database.messages.insert_one(data)
    chats= get_chat(main_user, username)
    return chats


# gets 2 user names and returns chat history between them
def get_chat(main_user: str, username: str):
    all_msgs=[]
    datas=database.messages.find()
    for data in datas:
        if (data["from"]==main_user and data["to"]==username):
            all_msgs.append(data)
        if (data["to"]==main_user and data["from"]==username):
            all_msgs.append(data)
    return all_msgs


#get profile picture for all online users
#returns dictionary of all users and pfp accociated with them
def get_all_pfps(users: list):
    user_pfps={}
    for user in users:
        profile = database.user_profiles.find_one({'username': user})
        if(profile["pfp"][0:7]=="static/" and profile["pfp"][7:13]=="avatar" and profile["pfp"][7:14]!="avatars"):
            user_pfps[user]=profile["pfp"][0:7] + "avatars/" + profile["pfp"][7:]
        else:
            user_pfps[user]=profile["pfp"]
    return user_pfps

list_msg=[]

def receive_notification(to_user: str, from_user: str):
    does_exist=False
    for each_msg in list_msg:
        if (each_msg == ([from_user,to_user])):
            does_exist=True
    if(does_exist == False):
        list_msg.append([from_user,to_user])
    -1

def send_list_msg():
    return list_msg

def fix_list_msg(from_user: str, to_user:str):
    does_exist=False
    for each_msg in list_msg:
        if (each_msg == ([from_user,to_user])):
            does_exist=True
    if(does_exist == True):
        list_msg.remove([from_user,to_user])
    -1