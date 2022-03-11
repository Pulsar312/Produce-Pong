from typing import List
from food.Ingredient import Ingredient

cheese = Ingredient("cheese", "Cheese", "cheese.png")
tomato = Ingredient("tomato", "Tomato", "tomato.png")
lettuce = Ingredient("lettuce", "Lettuce", "lettuce.png")
carrot = Ingredient("carrot", "carrot", "carrot.png")
noodles = Ingredient("noodles", "Noodles", "noodles.png")
hot_sauce = Ingredient("hot_sauce", "Hot Sauce", "hot_sauce.png")

ALL_INGREDIENTS: List[Ingredient] = [cheese, tomato, lettuce, carrot, noodles, hot_sauce]
# TODO find a better way to build ALL_INGREDIENTS
