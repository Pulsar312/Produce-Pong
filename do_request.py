import json
import sys

from flask import jsonify


# method which signs user in (signs up if necessary)
# returns the id of the user (or -1 if invalid)
def sign_in(request, users, count_users):
    print(request)
    data = json.loads(request.data)  # Note: request.get_json() doesn't word for some reason...

    if users.count_documents({'username': data['username']}) == 0:  # username not in database, so create a new user

        # Get the next id
        user_id = -1
        if count_users.count_documents({}) == 0:  # if theres no users created yet, then the first id will be 1
            count_users.insert_one({"id_num": 1})
            user_id = 1
        else:  # otherwise, we have some users already, so we get the previous id, and update our database
            result = count_users.find_one({})
            previous_id = result["id_num"]
            new_value = {"$set": {"id_num": previous_id + 1}}
            count_users.update_one({}, new_value)
            user_id = previous_id + 1

        data['id'] = user_id  # set the id for the user
        users.insert_one(data)  # insert the user
        result = users.find_one({'username': data['username'], 'password': data['password']})
        print("User created with id:  ", result['id'])  # just making sure it works
        return jsonify({'id': result['id']})  # returns the id to save as a cookie
    elif users.count_documents({'username': data['username'], 'password': data['password']}) == 1:  # username and password exist in the database, so sign user in
        result = users.find_one({'username': data['username'], 'password': data['password']})
        print("User found with id:  ", result['id'])  # just making sure it works
        return jsonify({'id': result['id']})  # returns the id to save as a cookie
    else:  # username must be in database, but password doesn't match, so can't sign in
        print("Could not sign in, invalid username or password")
        return jsonify({'id': -1})  # returns the invalid id
