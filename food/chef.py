from typing import List

from food import Ingredient


# TODO: Replace this class with the actual user!
class Chef:
    def __init__(self):
        self.ingredients: List[Ingredient] = []

    def add_ingredient(self, ingredient: Ingredient):  # adds the ingredient to the list of ingredients
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)
