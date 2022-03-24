from typing import List

from food import Recipe


class Ingredient:
    def __init__(self, name: str):
        self.name = name
        self.main_recipes: List[Recipe] = []
        self.extra_recipes: List[Recipe] = []

    # Method to add a recipe in which the ingredient is a main ingredient
    def add_main_recipes(self, recipe: Recipe):
        if recipe not in self.main_recipes:  # if we haven't added the recipe yet, then add it
            self.main_recipes.append(recipe)

    # Method to add a recipe in which the ingredient is an extra ingredient
    def add_extra_recipes(self, recipe: Recipe):
        if recipe not in self.extra_recipes:  # if we haven't added the recipe yet, then add it
            self.extra_recipes.append(recipe)

    # method prints out all ingredients with the recipes
    def to_string(self):
        str = "Name: " + self.name

        str += "\t\t\t\t\t"
        str += "Main Recipes: ["
        for r in self.main_recipes:
            str += r.name + ", "
        if str[len(str) - 1] != "[":
            str = str[:len(str) - 2]
        str = str + "]"

        str += "\t\t\t\t\t"
        str += "Extra Recipes: ["
        for r in self.extra_recipes:
            str += r.name + ", "
        if str[len(str) - 1] != "[":
            str = str[:len(str) - 2]
        str = str + "]"

        return str
