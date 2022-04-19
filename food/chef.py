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
        if database.achievements.count_documents({"username": username,"recipe":recipe.name}) == 0:
            database.achievements.insert_one({"username": username, "recipe": recipe.name})
            return True
        else:
            return False