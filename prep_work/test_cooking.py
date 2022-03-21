
# Note: This is a testing file for converting the json recipes into objects, and back into json.
import json

from food.Cooking import Cooking

if __name__ == '__main__':
    my_cooking: Cooking = Cooking('recipes.json')

    ingr = list(my_cooking.ingredients)
    print(ingr)
    print("ingr length: ", len(ingr))


    print(my_cooking.ingredients)
    for i in my_cooking.ingredients:
        print(my_cooking.ingredients[i].to_string())

    print("\n\n\n")

    for r in my_cooking.recipes:
        print(my_cooking.recipes[r].to_string())

