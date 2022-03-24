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


def test_find_recipes(cooking):
    chef1 = Chef()
    chef2 = Chef()

    for j in range(0, 20):
        print()
        i = cooking.get_random_ingredient(chef1, chef2)
        chef1.add_ingredient(i)

    print("chef1: ", end="\t\t")
    for k in chef1.ingredients:
        print(k.name, end=", ")
    print()

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")

def test_all_recipe_scores(cooking):
    chef1 = Chef()
    for i in cooking.ingredients:
        chef1.add_ingredient(cooking.ingredients[i])

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")
    print()
    print("Total recipes: ", len(rec))

    cooking.get_recipes_scores_from_ingredients(chef1.ingredients)

def test_one_recipe_score(cooking):
    chef1 = Chef()
    recipe = cooking.recipes["Pizza"]
    for i in recipe.main_ingredients:
        chef1.add_ingredient(i)

    print("chef1: ", end="\t\t")
    for k in chef1.ingredients:
        print(k.name, end=", ")
    print()
    print("Total ingredients: ", len(chef1.ingredients))

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")
    print()
    print("Total recipes: ", len(rec))

    print("-------- SCORES ---------")
    scores = cooking.get_recipes_scores_from_ingredients(chef1.ingredients)
    for j in scores:
        print(j.name, ": ", scores[j])

def test_alternative_and_extra(cooking):
    chef1 = Chef()
    recipe = cooking.recipes["Fried Rice"]
    for i in recipe.main_ingredients:
        if(i.name != "sesame oil"):
            chef1.add_ingredient(i)
    for i in recipe.alternative_ingredients:
        if(recipe.alternative_ingredients[i].name == "vegetable oil"):
            chef1.add_ingredient(recipe.alternative_ingredients[i])
    for i in recipe.extra_ingredients:
        chef1.add_ingredient(i)
    print("chef1: ", end="\t\t")
    for k in chef1.ingredients:
        print(k.name, end=", ")
    print()
    print("Total ingredients: ", len(chef1.ingredients))

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")
    print()
    print("Total recipes: ", len(rec))

    print("-------- SCORES ---------")
    scores = cooking.get_recipes_scores_from_ingredients(chef1.ingredients)
    for j in scores:
        print(j.name, ": ", scores[j])

if __name__ == '__main__':
    cooking: Cooking = Cooking('recipes.json')
    # print_ingredients_and_recipes(cooking)
    # test_get_random_ingredient(cooking)
    # test_find_recipes(cooking)
    test_all_recipe_scores(cooking)
    # test_one_recipe_score(cooking)
    # test_alternative_and_extra(cooking)
