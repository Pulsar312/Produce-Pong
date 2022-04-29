import database

# Adds an achievement to the achievements database if not there yet
# returns True if an achievement was added, and False if an achievement was not added
from food import Recipe


def add_achievement(username: str, recipe: Recipe):
    if database.achievements.count_documents({"username": username, "recipe": recipe.name}) == 0:
        database.achievements.insert_one({"username": username, "recipe": recipe.name, "recipe_image": recipe.get_recipe_image()})
        return True
    else:
        return False


def get_player_achievements(username: str):
    user_achievement = database.achievements.find({"username": username}, {"_id": 0, "username": 0})
    return list(user_achievement)
