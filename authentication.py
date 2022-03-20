import secrets
from typing import Tuple

from flask import render_template, make_response

# Get the login page for the initial page request
import database
import authentication_variables as av


def get_login_page():
    return render_template("div_templates/login.html")


# Return a secure string representing the password salted and hashed
def hash_password(password: str):
    # TODO actually implement salting and hashing
    return f"NOT_HASHED_{password}"


# Check if the provided password matches the secure string when salted and hashed
def check_password(clear_password: str, secure_string: str):
    # TODO this will need to account for hashing and salting in the future
    return hash_password(clear_password) == secure_string


# Check if the provided password matches the secure version stored in the database for this user
# Returns true if this user entered the correct password
def check_user_password(username: str, password: str):
    user = database.users.find_one({"username": username})
    secure_password = user["password"]  # Look up hashed password from database
    return check_password(password, secure_password)


# Check if a username already exists in the database
def user_exists(username: str) -> bool:
    return database.users.count_documents({"username": username}) != 0


# Create a new user in the database
# Returns a tuple containing a success boolean and an error message (safe for users to see)
def create_new_user(username: str, password: str) -> Tuple[bool, str]:
    if len(username) < av.MIN_USERNAME_LENGTH:
        return False, f"Usernames must be at least {av.MIN_USERNAME_LENGTH} characters long."

    if len(username) > av.MAX_USERNAME_LENGTH:
        return False, f"Usernames cannot be longer than {av.MAX_USERNAME_LENGTH} characters."

    for char in username:
        if char not in av.USERNAME_ALLOWED_CHARACTERS:
            return False, f"Usernames may only contain {av.USERNAME_ALLOWED_CHARACTERS_DESCRIPTION}."

    if user_exists(username):
        return False, f"The username '{username}' is already in use. Please choose a different one."

    if len(password) < av.MIN_PASSWORD_LENGTH:
        return False, f"Your password must be at least {av.MIN_PASSWORD_LENGTH} characters long."

    # NEVER STORE THE CLEAR PASSWORD! ALWAYS SALT AND HASH IT!
    database.users.insert_one({"username": username, "password": hash_password(password)})
    return True, ""


# Get the value of the session token from a request
def get_session_cookie(request):
    if request.cookies and av.SESSION_COOKIE_NAME in request.cookies:
        return request.cookies[av.SESSION_COOKIE_NAME]
    return None


# Get the user's username based on their request session cookie
# Returns an empty string they're not logged in
def get_username(request):
    cookie = get_session_cookie(request)
    if cookie:
        session = database.sessions.find_one({"token": cookie})
        if session:
            return session["username"]

    return ""


def generate_random_string(length: int = 1024):
    return secrets.token_urlsafe(length)


# Create a session for the provided username and return the session cookie value
def create_session(username: str):
    token = generate_random_string()
    database.sessions.insert_one({"username": username, "token": token})
    return token


# Delete one session to invalidate a cookie after manually logging out
def delete_session(token: str):
    database.sessions.delete_one({"token": token})


# Remove all sessions from username, to "log them out everywhere"
def delete_all_sessions(username: str):
    database.sessions.delete_many({"username": username})


# Set a cookie securely on a response object from make_response()
def set_secure_cookie(resp, cookie_name, cookie_value):
    resp.set_cookie(cookie_name, cookie_value, secure=True, httponly=True, samesite="Strict")


# Handle login form being submitted
# If successful login, make a session, set their cookie, return a partial template with some JavaScript commands
# If unsuccessful, return the login form again, but with an error message
def handle_login(request):
    data = request.form
    username = data["username"]
    password = data["password"]

    if user_exists(username):
        success = check_user_password(username, password)
        if success:
            # Successful login
            data = {"username": username}
            resp = make_response(render_template("div_templates/after_login.html", **data))
            set_secure_cookie(resp, av.SESSION_COOKIE_NAME, create_session(username))
            return resp
        else:
            # Wrong password
            data = {"error": "If you're trying to sign in, that was the incorrect password. Please try again. If you're trying to sign up, that username is already taken, so please try a different one."}
            return render_template("div_templates/login.html", **data)

    else:
        # User doesn't exist, so sign up
        create_success, create_message = create_new_user(username, password)
        if create_success:
            # New user successfully created
            data = {"username": username, "new_account": True}
            resp = make_response(render_template("div_templates/after_login.html", **data))
            set_secure_cookie(resp, av.SESSION_COOKIE_NAME, create_session(username))
            return resp
        else:
            # Signup failed for some reason explained in create_message
            data = {"error": f"Error creating new account. {create_message}"}
            return render_template("div_templates/login.html", **data)


def handle_logout(request):
    resp = make_response(render_template("div_templates/logged_out.html"))

    # Delete the session
    cookie = get_session_cookie(request)
    delete_session(cookie)

    # Erase the client's cookie
    resp.delete_cookie(av.SESSION_COOKIE_NAME)

    return resp
