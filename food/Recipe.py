import math
from typing import List
from typing import Dict

from food import Ingredient


class Recipe:
    def __init__(self,
                 name: str,
                 image_name: str = ""):
        self.name: str = name  # Name of the recipe
        self.main_ingredients: List[Ingredient] = []  # list of the main ingredients in the recipe
        self.alternative_ingredients: Dict[Ingredient, Ingredient] = {}  # dictionary of the alternatives (substituted -> substitution), substituted should be in the main ingredients
        self.extra_ingredients: List[Ingredient] = []  # list of all the extra ingredients
        self.image_name = image_name  # TODO: name of the recipe's image

    # Method to add a main ingredient to the recipe
    def add_main_ingredient(self, ingredient: Ingredient):
        if ingredient not in self.main_ingredients:  # make sure not in main ingredient list yet
            self.main_ingredients.append(ingredient)  # add the main ingredient

    # Method to add an extra ingredient to the recipe
    def add_extra_ingredient(self, ingredient: Ingredient):
        if ingredient not in self.extra_ingredients:  # make sure not in extra ingredient list yet
            self.extra_ingredients.append(ingredient)  # add the extra ingredient

    # Method to add an alternative ingredient to the recipe
    def add_alternative(self, substituted: Ingredient, substitution: Ingredient):
        if substituted in self.main_ingredients:  # make sure the substituted ingredient is in main ingredients
            if substituted not in self.alternative_ingredients:  # make sure pairing is not in alternative ingredients yet (Note: cannot have two alternatives for the same main ingredient)
                self.alternative_ingredients[substituted] = substitution  # add to the alternative ingredients

    # Method to get the score for the recipe based on the user's current ingredients and the total ingredient occurrence (from Cooking)
    def get_score_from_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = (self.get_score_from_main_ingredients(ingredients, total_ingredient_occurrence) + self.get_score_from_extra_ingredients(ingredients, total_ingredient_occurrence)) * 2  # get the score for the recipe based on main ingredients and extra ingredients (Note: multiply by 2 just for wider distribution of scores)
        return total_score

    # Method to get the score for the recipe based on the main ingredients
    def get_score_from_main_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = 0  # start with a score of 0, and add on to it
        for i in self.main_ingredients:  # for each main ingredient in the recipe,
            if i not in ingredients and ((i not in self.alternative_ingredients) or (i in self.alternative_ingredients and self.alternative_ingredients[i] not in ingredients)):  # if we don't have the ingredient or a substitution for the ingredient
                return 0  # missing a main ingredient gives immediate 0 score, should never happen
            elif i not in ingredients and i in self.alternative_ingredients and self.alternative_ingredients[i] in ingredients:  # if we don't have the ingredient, but we do have the alternative
                alt = self.alternative_ingredients[i]  # get the alternative ingredient
                this_ingredient_occurrence = len(alt.main_recipes) + (len(alt.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes (gives more variation in scores)
                probability_not_getting_ingredient = (total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence  # approximate probability of not getting the ingredient (high frequency -> low scores, low frequency -> high scores)
                score = math.pow(probability_not_getting_ingredient, math.pow(this_ingredient_occurrence, 2))  # lower the score based on ingredient frequency, and lower drastically since its an alternative
                total_score += score  # add to the cumulative score
            else:
                this_ingredient_occurrence = len(i.main_recipes) + (len(i.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes (gives more variation in scores)
                probability_not_getting_ingredient = (total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence  # approximate probability of not getting the ingredient (high frequency -> low scores, low frequency -> high scores)
                score = math.pow(probability_not_getting_ingredient, this_ingredient_occurrence)  # lower the score based on ingredient frequency
                total_score += score

        return total_score

    # Method to get the score for the recipe based on the extra ingredients
    def get_score_from_extra_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = 0
        for i in self.extra_ingredients:  # for each of the possible extra ingredients
            if i in ingredients:  # if we actually have that extra ingredient
                this_ingredient_occurrence = len(i.main_recipes) + (len(i.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes
                probability_not_getting_ingredient = (total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence  # approximate probability of not getting the ingredient (high frequency -> low scores, low frequency -> high scores)
                score = 0.25 * math.pow(probability_not_getting_ingredient, math.pow(this_ingredient_occurrence, 2))  # drastically lower the score based on ingredient frequency, and only add a quarter since we want the extra ingredients to just give a small boost
                total_score += score
        return total_score

    # method returns a string of all recipes with their ingredients
    def to_string(self):
        ret_str = "Name: " + self.name

        ret_str += "\t\t\t\t\t"
        ret_str += "Main Ingredients: ["
        for i in self.main_ingredients:
            ret_str += i.name + ", "
        if ret_str[len(ret_str) - 1] != "[":
            ret_str = ret_str[:len(ret_str) - 2]
        ret_str = ret_str + "]"

        ret_str += "\t\t\t\t\t"
        ret_str += "Extra Ingredients: ["
        for i in self.extra_ingredients:
            ret_str += i.name + ", "
        if ret_str[len(ret_str) - 1] != "[":
            ret_str = ret_str[:len(ret_str) - 2]
        ret_str = ret_str + "]"

        ret_str += "\t\t\t\t\t"
        ret_str += "Alternative Ingredients: ["
        for i in self.alternative_ingredients:
            ret_str += self.alternative_ingredients[i].name + ", "
        if ret_str[len(ret_str) - 1] != "[":
            ret_str = ret_str[:len(ret_str) - 2]
        ret_str = ret_str + "]"

        return ret_str
