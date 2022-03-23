import random

def sign_up(username, user_profiles):
    random_init = random.randint(1,8)
    user_profiles.insert_one({'username': username, 'pfp': 'static/avatar'+str(random_init)+'.jpg'})
    