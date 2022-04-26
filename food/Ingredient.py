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

    def get_ingredient_image(self):
        image_name = self.name.replace(" ", "_").replace("\'", "").replace("\"", "").lower() + ".png"
        return image_name

    def to_dict(self):
        return {"name": self.name, "image": self.get_ingredient_image()}

    # method returns a string of all ingredients with their recipes
    def to_string(self):
        ret_str = "Name: " + self.name

        ret_str += "\t\t\t\t\t"
        ret_str += "Main Recipes: ["
        for r in self.main_recipes:
            ret_str += r.name + ", "
        if ret_str[len(ret_str) - 1] != "[":
            ret_str = ret_str[:len(ret_str) - 2]
        ret_str = ret_str + "]"

        ret_str += "\t\t\t\t\t"
        ret_str += "Extra Recipes: ["
        for r in self.extra_recipes:
            ret_str += r.name + ", "
        if ret_str[len(ret_str) - 1] != "[":
            ret_str = ret_str[:len(ret_str) - 2]
        ret_str = ret_str + "]"

        return ret_str
