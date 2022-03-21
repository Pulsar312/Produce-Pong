import json

from food.Ingredient import Ingredient
from food.Recipe import Recipe


class Cooking:
    def __init__(self, filename):
        self.recipes = {}
        self.ingredients = {}
        self.setup_cooking(filename)

    def setup_cooking(self, filename):
        content = json.loads(open(filename, 'r').read())  # read the file into json

        for recipe in content:  # create a recipe for every element in json file
            new_recipe = self.create_recipe(recipe)
            self.recipes[new_recipe.name] = new_recipe

    def create_recipe(self, json_recipe):
        json_recipe_name = json_recipe["recipe_name"]
        json_main_ingredients = json_recipe["main_ingredients"]
        json_extra_ingredients = json_recipe["extra_ingredients"]
        json_alternative_ingredients = json_recipe["alternative_ingredients"]

        recipe = Recipe(json_recipe_name)

        for i in json_main_ingredients:
            ingredient = self.get_ingredient(i)
            recipe.add_main_ingredient(ingredient)
            ingredient.add_recipes(recipe)

        for i in json_extra_ingredients:
            ingredient = self.get_ingredient(i)
            recipe.add_extra_ingredient(ingredient)
            ingredient.add_recipes(recipe)

        for (key_substituted, value_substitution) in json_alternative_ingredients:
            substituted = self.get_ingredient(key_substituted)
            substitution = self.get_ingredient(value_substitution)
            recipe.add_alternative(substituted, substitution)
            substitution.add_recipes(recipe) #note substituted should already be in ingredients list from earlier for loop

        return recipe

    # Create or get an ingredient
    def get_ingredient(self, name):
        if (name in self.ingredients):  # if ingredient exists, then just retrieve it
            return self.ingredients[name]
        else:
            new_ingredient = Ingredient(name)  # else, if it doesnt exist, then create it and add it to ingredients list
            self.ingredients[name] = new_ingredient
            return new_ingredient
