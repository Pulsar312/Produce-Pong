from typing import List
from food.old_food.Food import Food
from food.old_food.Substitution import Substitution
from food.old_food.ingredients import cheese, noodles, hot_sauce, lettuce, carrot, tomato

optional_hot_sauce = Substitution([], hot_sauce, 0)
tomatoes_are_bad_cheese_is_good = Substitution([tomato], [cheese], 5)

ALL_FOODS: List[Food] = [
    Food("mac_and_cheese",
         "Macaroni and Cheese",
         ingredients=[cheese, noodles],
         substitutions=[optional_hot_sauce],
         image_name="mac.png"),

    Food("salad",
         "Salad",
         ingredients=[lettuce, carrot, tomato],
         substitutions=[tomatoes_are_bad_cheese_is_good],
         image_name="salad.png")
]
