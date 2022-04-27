from typing import List

from food import Ingredient, Recipe
import database


class Chef:
    def __init__(self):
        self.ingredients: List[Ingredient] = []

    # Adds the ingredient to the list of ingredients
    def add_ingredient(self, ingredient: Ingredient):
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)

    # Adds an achievement to the achievements database if not there yet
    # returns True if an achievement was added, and False if an achievement was not added
    def add_achievement(self, username: str, recipe: Recipe):
        if database.achievements.count_documents({"username": username,"recipe": recipe.name}) == 0:
            database.achievements.insert_one({"username": username, "recipe": recipe.name, "recipe_image": recipe.get_recipe_image()})
            return True
        else:
            return False

    def get_player_achievements(self, username: str):
        user_achievement = database.achievements.find({"username": username}, {"_id":0, "username":0})
        return list(user_achievement)




    def to_dict(self):
        ing_list = []
        for i in self.ingredients:
            ing_list.append(i.to_dict())
        return {"ingredients":ing_list}