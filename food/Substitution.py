from food.Ingredient import Ingredient
from typing import List


class Substitution:
    def __init__(self, original_ingredients: List[Ingredient],
                 new_ingredients: List[Ingredient],
                 value_change: float):
        """
        Creates a Substitution of zero, one, or more ingredients for another set of zero, one, or more ingredients
        :param original_ingredients: The list of ingredients that will be removed if this substitution is applied
        :param new_ingredients: The list of ingredients that will be inserted
        :param value_change: How does this substitution affect the quality of the recipe? Negative values are bad substitutions, positive values are good substitutions.
        """
        self.value_change = value_change
        self.new_ingredients = new_ingredients
        self.original_ingredients = original_ingredients

    # TODO everything else
