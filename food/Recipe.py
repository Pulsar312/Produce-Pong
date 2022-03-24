import math
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

    def get_score_from_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = (self.get_score_from_main_ingredients(ingredients, total_ingredient_occurrence) + self.get_score_from_extra_ingredients(ingredients, total_ingredient_occurrence)) * 2
        # print("{:<5s}{:<40s}{:<7s}{:<5.4f}".format("Recipe: ", self.name, "score: ", total_score))
        # print("-------------------------------------------------------------")
        return total_score

    def get_score_from_main_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = 0
        for i in self.main_ingredients:
            if (i not in ingredients and ((i not in self.alternative_ingredients) or (i in self.alternative_ingredients and self.alternative_ingredients[i] not in ingredients))):
                return 0  # missing a main ingredient gives immediate 0 score, should never happen
            elif (i not in ingredients and i in self.alternative_ingredients and self.alternative_ingredients[i] in ingredients):
                # print("Alternative!")
                alt = self.alternative_ingredients[i]
                this_ingredient_occurrence = len(alt.main_recipes) + (len(alt.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes
                score = math.pow((total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence, math.pow(this_ingredient_occurrence, 2))  # lower the score since its an alternative!
                # print("{:<10s}{:<24s}{:<7s}{:<5.4f}".format("ingredient: ", alt.name, "score: ", score))
                total_score += score
            else:
                this_ingredient_occurrence = len(i.main_recipes) + (len(i.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes
                score = math.pow((total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence, this_ingredient_occurrence)
                # print("{:<10s}{:<24s}{:<7s}{:<5.4f}".format("ingredient: ", i.name, "score: ", score))
                total_score += score
        # for i in self.extra_ingredients:
        #     if
        # print("{:<5s}{:<40s}{:<7s}{:<5.4f}".format("Main: ", self.name, "score: ", total_score))
        # print("-")
        return total_score

    def get_score_from_extra_ingredients(self, ingredients, total_ingredient_occurrence):
        total_score = 0
        for i in self.extra_ingredients:
            if i in ingredients:
                this_ingredient_occurrence = len(i.main_recipes) + (len(i.extra_recipes) * 0.5)  # weigh the main_recipes more than the extra_recipes
                score = 0.25 * math.pow((total_ingredient_occurrence - this_ingredient_occurrence) / total_ingredient_occurrence, math.pow(this_ingredient_occurrence,2)) # make the scores
                # print("{:<10s}{:<24s}{:<7s}{:<5.4f}".format("ingredient: ", i.name, "score: ", score))
                total_score += score
        # for i in self.extra_ingredients:
        #     if
        # print("{:<5s}{:<40s}{:<7s}{:<5.4f}".format("Extra: ", self.name, "score: ", total_score))
        # print("-")
        return total_score

    # method prints out all recipes with the ingredients
    def to_string(self):
        str = "Name: " + self.name

        str += "\t\t\t\t\t"
        str += "Main Ingredients: ["
        for i in self.main_ingredients:
            str += i.name + ", "
        if str[len(str) - 1] != "[":
            str = str[:len(str) - 2]
        str = str + "]"

        str += "\t\t\t\t\t"
        str += "Extra Ingredients: ["
        for i in self.extra_ingredients:
            str += i.name + ", "
        if str[len(str) - 1] != "[":
            str = str[:len(str) - 2]
        str = str + "]"

        str += "\t\t\t\t\t"
        str += "Alternative Ingredients: ["
        for i in self.alternative_ingredients:
            str += self.alternative_ingredients[i].name + ", "
        if str[len(str)-1] != "[":
            str = str[:len(str) - 2]
        str = str + "]"

        return str
