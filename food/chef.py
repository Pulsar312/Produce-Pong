from typing import List

from food import Ingredient


class Chef:
    def __init__(self):
        self.ingredients: List[Ingredient] = []

    def add_ingredient(self, ingredient: Ingredient):
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)



