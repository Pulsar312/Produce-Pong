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

    def to_dict(self):
        ing_list = []
        for i in self.ingredients:
            ing_list.append(i.to_dict())
        return {"ingredients": ing_list}
