# Note: This is a testing file for converting the json recipes into objects, and back into json.
import json

from food.Cooking import Cooking
from food.chef import Chef


def print_ingredients_and_recipes(my_cooking):
    ingr = list(my_cooking.ingredients)
    print(ingr)
    print("ingr length: ", len(ingr))

    print(my_cooking.ingredients)
    for i in my_cooking.ingredients:
        print(my_cooking.ingredients[i].to_string())

    print("\n\n\n")

    for r in my_cooking.recipes:
        print(my_cooking.recipes[r].to_string())


def test_get_random_ingredient(cooking):
    chef1 = Chef()
    chef2 = Chef()

    for j in range(0, 10):
        print()
        print()
        i = cooking.get_random_ingredient(chef1, chef2)
        chef1.add_ingredient(i)

        print("chef1: ", end="\t\t")
        for k in chef1.ingredients:
            print(k.name, end=", ")
        print()
        print("chef2: ", end="\t\t")
        for k in chef2.ingredients:
            print(k.name, end=", ")
        print()

        i = cooking.get_random_ingredient(chef1, chef2)
        chef2.add_ingredient(i)

        print("chef1: ", end="\t\t")
        for k in chef1.ingredients:
            print(k.name, end=", ")
        print()
        print("chef2: ", end="\t\t")
        for k in chef2.ingredients:
            print(k.name, end=", ")
        print()


if __name__ == '__main__':
    cooking: Cooking = Cooking('recipes.json')
    # print_ingredients_and_recipes(cooking)
    # test_get_random_ingredient(cooking)

