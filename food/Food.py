from typing import List
import Ingredient
from food import Substitution


class Food:
    def __init__(self, technical_name: str,
                 friendly_name: str,
                 ingredients: List[Ingredient] = None,
                 substitutions: List[Substitution] = None,
                 image_name: str = ""):
        self.image_name = image_name
        self.substitutions = substitutions
        self.ingredients = ingredients
        self.friendly_name = friendly_name
        self.technical_name = technical_name

    # TODO a lot more
