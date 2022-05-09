import json
import random
from typing import List, Dict, Tuple, Optional

from food.Ingredient import Ingredient
from food.Recipe import Recipe
from food.chef import Chef


class Cooking:
    def __init__(self, filename):
        self.recipes: Dict[str, Recipe] = {}  # all of the recipes we have
        self.ingredients: Dict[str, Ingredient] = {}  # all of the ingredients we have
        self.total_ingredient_occurrence: int = 0  # the total number of times the ingredients occur (151 if using the current recipes); this is used to calculate scores (and saves on runtime so that we dont need to recalculate every time)
        self.setup_cooking(filename)  # set up all the above variables

    def setup_cooking(self, filename: str):
        content = json.loads(open(filename, 'r').read())  # read the file into json

        for recipe in content:
            new_recipe: Recipe = self.create_recipe(recipe)  # create a recipe for every element in json file
            self.recipes[new_recipe.name] = new_recipe  # add the recipe to map

    def get_image_from_name(self, name: str):
        image_name = ""
        if name in self.recipes:
            image_name = "../static/recipes/" + name.replace(" ", "_").replace("\'", "").replace("\"", "").lower() + ".png"
        elif name in self.ingredients:
            image_name = "../static/ingredients/" + name.replace(" ", "_").replace("\'", "").replace("\"", "").lower() + ".png"
        else:
            print("Not found: ", name)

        return image_name

    # create recipes
    def create_recipe(self, json_recipe: json):
        recipe = Recipe(json_recipe["recipe_name"])  # create a Recipe
        self.add_all_main_ingredients(recipe, json_recipe["main_ingredients"])  # add the main ingredients
        self.add_all_extra_ingredients(recipe, json_recipe["extra_ingredients"])  # add the extra ingredients
        self.add_all_alternative_ingredients(recipe, json_recipe["alternative_ingredients"])  # add the alternative ingredients

        return recipe

    def add_all_main_ingredients(self, recipe: Recipe, json_main_ingredients: json):
        for i in json_main_ingredients:  # add all the main ingredients
            self.total_ingredient_occurrence += 1  # we see ingredient, we add to counter
            ingredient = self.get_ingredient(i)  # create or get the ingredient
            recipe.add_main_ingredient(ingredient)  # add the ingredient to recipe's main ingredients
            ingredient.add_main_recipes(recipe)  # add the recipe to the ingredient's main recipes list

    def add_all_extra_ingredients(self, recipe: Recipe, json_extra_ingredients: json):
        for i in json_extra_ingredients:  # add all the extra ingredients
            self.total_ingredient_occurrence += 1  # we see ingredient, we add to counter
            ingredient = self.get_ingredient(i)  # create or get the ingredient
            recipe.add_extra_ingredient(ingredient)  # add the ingredient to recipe's extra ingredients
            ingredient.add_extra_recipes(recipe)  # add the recipe to the ingredient's extra recipes list

    def add_all_alternative_ingredients(self, recipe: Recipe, json_alternative_ingredients: json):
        for (key_substituted, value_substitution) in json_alternative_ingredients:  # add all the alternative ingredients
            self.total_ingredient_occurrence += 1  # we see ingredient, we add to counter
            substituted = self.get_ingredient(key_substituted)  # create or get the ingredient that will be substituted
            substitution = self.get_ingredient(value_substitution)  # create or get the ingredient that will be the substitution
            recipe.add_alternative(substituted, substitution)  # add the pair to the recipe's alternative ingredients
            substitution.add_main_recipes(recipe)  # Add the recipe to the substitution's main recipes (since substitutions can only happen for main ingredients). Note: substituted should already be in ingredients list from earlier for loop, if not, then the json file is not formatted properly

    # Create or get an ingredient
    def get_ingredient(self, name: str):
        if name in self.ingredients:  # if ingredient exists, then just retrieve it
            return self.ingredients[name]
        else:
            new_ingredient = Ingredient(name)  # else, if it doesnt exist, then create it and add it to ingredients list
            self.ingredients[name] = new_ingredient
            return new_ingredient

    # Get a random ingredient for pong-ing
    def get_random_ingredient(self, chef1: Chef, chef2: Chef):  # need to have both users (to access their ingredient lists)
        ingredient_list: List[Ingredient] = list(self.ingredients.values())  # list of ingredients to pick from
        # figure out min and max lists, so that shorter runtime of for loop
        updated_total = self.total_ingredient_occurrence  # in case of ingredient removal

        min_chef_list = []
        max_chef_list = []

        if len(chef1.ingredients) > len(chef2.ingredients):
            min_chef_list = chef2.ingredients
            max_chef_list = chef1.ingredients
        else:
            min_chef_list = chef1.ingredients
            max_chef_list = chef2.ingredients

        # for loop to go through and remove same ingredients (so that we don't get the same ingredient if they both have that ingredient
        for i in min_chef_list:  # for each of the ingredients for chef1
            if i in max_chef_list:  # if chef2 also has that ingredient,
                updated_total -= (len(i.main_recipes) + len(i.extra_recipes))  # lower the total ingredient occurrence, so that we don't go past the length of our list
                ingredient_list.remove(i)  # remove ingredient from our list of ingredients to pick from

        if len(ingredient_list) == 0:  # this should really never happen, if theres no ingredients left in the list, then both people should have a dish
            return None

        random_num = random.randint(0, updated_total - 2)  # get a random ingredient

        ingredient_index = 0  # start at index 0 to find ingredient
        while random_num >= (len(ingredient_list[ingredient_index].main_recipes) + len(ingredient_list[ingredient_index].extra_recipes)):  # calculate which ingredient to get
            random_num -= (len(ingredient_list[ingredient_index].main_recipes) + len(ingredient_list[ingredient_index].extra_recipes))  # decrease random_num until 0. decreasing by the number of recipes the given ingredient occurs in (more common ingredients are more likely to get chosen this way, while rare-er ingredients are less likely to get chosen)
            ingredient_index += 1  # increment to our next ingredient

        return ingredient_list[ingredient_index]  # return the ingredient at the calculated index

    # Get all possible recipes from the list of ingredients
    def get_recipes_from_ingredient_list(self, ing: List[Ingredient]):

        potential_recipe_list: List[Recipe] = []  # list of recipes we might be able to get

        for i in ing:  # for each of the ingredients we have,
            for r in i.main_recipes:  # for each of the recipes for the ingredient,
                if r not in potential_recipe_list:  # if we haven't added the recipe yet,
                    potential_recipe_list.append(r)  # then we add the recipe to double check it later

        filtered_recipes: List[Recipe] = []  # list of recipes we have all ingredients for
        for r in potential_recipe_list:  # go through every potential recipe
            has_all_ingredients = True  # by default, assume we have all the ingredients
            for i in r.main_ingredients:  # go through the main ingredients for the recipe
                if i not in ing:  # if we don't have a main ingredient
                    if (i in r.alternative_ingredients) and (r.alternative_ingredients[i] not in ing):  # if there exists an alternative for the ingredient, but we don't actually have that alternative
                        has_all_ingredients = False  # we know we don't have the ingredient, so we set False, and break out of the loop
                        break
                    elif i not in r.alternative_ingredients:  # if there is no alternative for this ingredient
                        has_all_ingredients = False  # we know we don't have the ingredient, so we set False, and break out of the loop
                        break

            if has_all_ingredients:  # if our assumption that we have the ingredient is still true (we haven't not found a main ingredient)
                filtered_recipes.append(r)  # append to our filtered recipes.

        return filtered_recipes  # return the filtered list of recipes

    # Method to get all the scores for each recipe
    # Returns a dictionary of recipe -> score
    def get_recipes_scores_from_ingredients(self, ingredients: List[Ingredient], recipes: List[Recipe] = None):
        if recipes is None:  # if we didn't specify a list of recipes,
            recipes = self.get_recipes_from_ingredient_list(ingredients)  # then we go and find the list of recipes that we can construct

        scores: Dict[Recipe, float] = {}
        for r in recipes:
            scores[r] = r.get_score_from_ingredients(ingredients, self.total_ingredient_occurrence)  # for each of the recipes, get the score based on the ingredients that we have, and add it to our map

        return scores

    # Method to get the recipe with the highest score
    # Returns recipe, score
    def get_best_recipe_and_score(self, ingredients: List[Ingredient], recipes: List[Recipe] = None) -> Tuple[Recipe, float]:
        score_dict: Dict[Recipe, float] = self.get_recipes_scores_from_ingredients(ingredients, recipes)  # get the dictionary of recipes->scores

        best_recipe: Optional[Recipe] = None
        best_score: float = 0.0
        for recipe in score_dict:
            if (best_recipe is None and best_score == 0) or (best_score < score_dict[recipe]):  # if we haven't found a recipe yet, or if the score is better than the score saved, then update best_recipe and best_score
                best_recipe = recipe
                best_score = score_dict[recipe]

        return best_recipe, best_score
