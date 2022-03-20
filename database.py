# Create database collections here, and pass as parameter
import os

import pymongo

client = pymongo.MongoClient(os.getenv("MONGO_HOST", "localhost"))
db = client.mydata
users = db.users  # creating/retrieving a collection for saving usernames and passwords
count_users = db.count_users  # creating/retrieving a collection for saving the amount of users we have
sessions = db.sessions  # Keep users logged in with cookies


def initialize():
    # Force this file to be run when the app is started
    # Import this file anywhere we need a db connection
    pass