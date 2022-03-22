import json
import random
from typing import List

from food.Ingredient import Ingredient
from food.Recipe import Recipe
from food.chef import Chef


class Cooking:
    def __init__(self, filename):
        self.recipes = {}
        self.ingredients = {}
        self.total_ingredient_occurrence = 0
        self.setup_cooking(filename)

    def setup_cooking(self, filename):
        content = json.loads(open(filename, 'r').read())  # read the file into json

        for recipe in content:  # create a recipe for every element in json file
            new_recipe = self.create_recipe(recipe)
            self.recipes[new_recipe.name] = new_recipe

    # create recipes
    def create_recipe(self, json_recipe):

        recipe = Recipe(json_recipe["recipe_name"])  # create a Recipe

        self.add_all_main_ingredients(recipe, json_recipe["main_ingredients"])
        self.add_all_extra_ingredients(recipe, json_recipe["extra_ingredients"])
        self.add_all_alternative_ingredients(recipe, json_recipe["alternative_ingredients"])

        return recipe

    def add_all_main_ingredients(self, recipe, json_main_ingredients):
        for i in json_main_ingredients:  # add all the main ingredients
            self.total_ingredient_occurrence += 1
            ingredient = self.get_ingredient(i)
            recipe.add_main_ingredient(ingredient)
            ingredient.add_main_recipes(recipe)

    def add_all_extra_ingredients(self, recipe, json_extra_ingredients):
        for i in json_extra_ingredients:  # add all the extra ingredients
            self.total_ingredient_occurrence += 1
            ingredient = self.get_ingredient(i)
            recipe.add_extra_ingredient(ingredient)
            ingredient.add_extra_recipes(recipe)

    def add_all_alternative_ingredients(self, recipe, json_alternative_ingredients):
        for (key_substituted, value_substitution) in json_alternative_ingredients:  # add all the alternative ingredients
            self.total_ingredient_occurrence += 1
            substituted = self.get_ingredient(key_substituted)
            substitution = self.get_ingredient(value_substitution)
            recipe.add_alternative(substituted, substitution)
            substitution.add_main_recipes(recipe)  # note substituted should already be in ingredients list from earlier for loop, if not, then the json file is not formatted properly

    # Create or get an ingredient
    def get_ingredient(self, name):
        if (name in self.ingredients):  # if ingredient exists, then just retrieve it
            return self.ingredients[name]
        else:
            new_ingredient = Ingredient(name)  # else, if it doesnt exist, then create it and add it to ingredients list
            self.ingredients[name] = new_ingredient
            return new_ingredient

    # Get next random ingredient
    def get_random_ingredient(self, chef1: Chef, chef2: Chef):
        ingredient_list: List[Ingredient] = list(self.ingredients.values())  # list of ingredients to pick from
        # figure out min and max lists, so that shorter runtime of for loop
        updated_total = self.total_ingredient_occurrence  # in case of ingredient removal

        global min_chef_list
        global max_chef_list

        min_chef_list = []
        max_chef_list = []

        if (len(chef1.ingredients) > len(chef2.ingredients)):
            min_chef_list = chef2.ingredients
            max_chef_list = chef1.ingredients
        else:
            min_chef_list = chef1.ingredients
            max_chef_list = chef2.ingredients

        # for loop to go through and remove same ingredients (so that we don't get the same ingredient if they both have that ingredient
        for i in min_chef_list:
            if i in max_chef_list:
                updated_total -= (len(i.main_recipes) + len(i.extra_recipes))  # lower the total ingredient occurance, so that we don't go past the length of our list
                ingredient_list.remove(i)  # remove ingredient from our list of ingredients to pick from

        if (len(ingredient_list) == 0):  # this should really never happen, if theres no ingredients left in the list, then both people should have a dish
            return None

        random_num = random.randint(0, updated_total - 1)

        ingredient_index = 0
        while (random_num >= (len(ingredient_list[ingredient_index].main_recipes) + len(ingredient_list[ingredient_index].extra_recipes))):  # calculate which ingredient to get
            random_num -= (len(ingredient_list[ingredient_index].main_recipes) + len(ingredient_list[ingredient_index].extra_recipes))
            ingredient_index += 1

        return ingredient_list[ingredient_index]  # return the ingredient at the correct index

    # Get all possible recipes from the list of ingredients
    def get_recipes_from_ingredient_list(self, ing: List[Ingredient]):

        sorted_ingredients = sorted(ing, key=lambda i: len(i.main_recipes), reverse=False)

        sorted_ingredients = [i for i in sorted_ingredients if len(i.main_recipes) != 0]

        # [print(i.name, end = ", ") for i in sorted_ingredients]
        # print()

        recipe_list = []

        for i in sorted_ingredients:
            for r in i.main_recipes:
                if r not in recipe_list:
                    recipe_list.append(r)

        filtered_recipes = []
        for r in recipe_list:
            has_all_ingredients = True
            for i in r.main_ingredients:
                if (i not in ing):
                    if (i in r.alternative_ingredients) and (r.alternative_ingredients[i] not in ing):
                        has_all_ingredients = False
                        break
                    elif i not in r.alternative_ingredients:
                        has_all_ingredients = False
                        break

            if has_all_ingredients:
                filtered_recipes.append(r)

        return filtered_recipes
