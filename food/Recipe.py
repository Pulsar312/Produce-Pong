from typing import List
from typing import Dict

from food import Ingredient


class Recipe:
    def __init__(self,
                 name: str,
                 image_name: str = ""):
        self.name = name
        self.main_ingredients = []
        self.alternative_ingredients = {}
        self.extra_ingredients = []
        self.image_name = image_name

    def add_main_ingredient(self, ingredient: Ingredient):
        self.main_ingredients.append(ingredient)

    def add_extra_ingredient(self, ingredient: Ingredient):
        self.extra_ingredients.append(ingredient)

    def add_alternative(self, ingredient_main: Ingredient, ingredient_alternative: Ingredient):
        self.alternative_ingredients[ingredient_main] = ingredient_alternative

    def to_string(self):
        str = "Name: " + self.name

        str += "\t\t\t\t\t"
        str += "Main Ingredients: ["
        for i in self.main_ingredients:
            str += i.name + ", "
        str = str[:len(str) - 2] + "]"

        str += "\t\t\t\t\t"
        str += "Extra Ingredients: ["
        for i in self.extra_ingredients:
            str += i.name + ", "
        str = str[:len(str) - 2] + "]"

        str += "\t\t\t\t\t"
        str += "Alternative Ingredients: ["
        for i in self.alternative_ingredients:
            str += self.alternative_ingredients[i].name + ", "
        str = str[:len(str) - 2] + "]"

        return str
