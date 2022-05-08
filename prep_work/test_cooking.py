# Note: This is a example usage file for food
import json
from pathlib import Path

from food.Cooking import Cooking
from food.Recipe import Recipe
from food.achievement_database import add_achievement, get_player_achievements
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

    print(len(cooking.ingredients))

    for j in range(0, 48):
        print()
        print(j)
        i = cooking.get_random_ingredient(chef1, chef2)
        chef1.add_ingredient(i)
        chef2.add_ingredient(i)

        # print("chef1: ", end="\t\t")
        # for k in chef1.ingredients:
        #     print(k.name, end=", ")
        # print()
        # print("chef2: ", end="\t\t")
        # for k in chef2.ingredients:
        #     print(k.name, end=", ")
        # print()

        # i = cooking.get_random_ingredient(chef1, chef2)
        # chef2.add_ingredient(i)

        # print("chef1: ", end="\t\t")
        # for k in chef1.ingredients:
        #     print(k.name, end=", ")
        # print()
        # print("chef2: ", end="\t\t")
        # for k in chef2.ingredients:
        #     print(k.name, end=", ")
        # print()

    list1 = []
    for k in chef1.ingredients:
        list1.append(k.name)
    list1.sort()
    print("sorted1: ", list1)

    list2 = []
    for k in chef2.ingredients:
        list2.append(k.name)
    list2.sort()
    print("sorted2:", list2)


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
        if (i.name != "sesame oil"):
            chef1.add_ingredient(i)
    for i in recipe.alternative_ingredients:
        if (recipe.alternative_ingredients[i].name == "vegetable oil"):
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


def test_get_top_recipe(cooking):
    chef1 = Chef()
    for i in cooking.ingredients:
        chef1.add_ingredient(cooking.ingredients[i])

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")
    print()
    print("Total recipes: ", len(rec))

    scores = cooking.get_recipes_scores_from_ingredients(chef1.ingredients)
    for (recipe) in scores:
        print("{:<35s}{:<10.4f}".format(recipe.name + ":", scores[recipe]))

    top_recipe, top_score = cooking.get_best_recipe_and_score(chef1.ingredients)

    print("Top recipe: ", top_recipe.name, ",    score: ", top_score)


def test_get_top_recipe_no_ingredients(cooking):
    chef1 = Chef()

    rec = cooking.get_recipes_from_ingredient_list(chef1.ingredients)
    print("recipes: ", end="\t\t")
    for r in rec:
        print(r.name, end=", ")
    print()
    print("Total recipes: ", len(rec))

    scores = cooking.get_recipes_scores_from_ingredients(chef1.ingredients)
    for (recipe) in scores:
        print("{:<35s}{:<10.4f}".format(recipe.name + ":", scores[recipe]))

    top_recipe, top_score = cooking.get_best_recipe_and_score(chef1.ingredients)

    print("Top recipe: ", top_recipe, ",    score: ", top_score)

def test_chef_to_dict(cooking):
    chef1 = Chef()
    recipe = cooking.recipes["Pizza"]
    for i in recipe.main_ingredients:
        chef1.add_ingredient(i)

    print(chef1.to_dict())

def test_ingredient_images(cooking):
    for i in cooking.ingredients:
        path_to_file = cooking.get_image_from_name(i)
        print(path_to_file)
        path = Path(path_to_file)
        try:
            assert(path.is_file())
        except:
            print("NOT FOUND: ", i)

def test_mongo(cooking):
    recipe = Recipe("soMe food's")
    add_achievement("sia", recipe)
    result = get_player_achievements("sia")
    print(result)

def debug_get_random_ingredient(cooking):
    print(len(cooking.recipes))
    print(len(cooking.ingredients))
    print(cooking.ingredients)
    print(cooking.get_random_ingredient(Chef(), Chef()))

if __name__ == '__main__':
    cooking: Cooking = Cooking('recipes.json')
    # print_ingredients_and_recipes(cooking)
    test_get_random_ingredient(cooking)
    # test_find_recipes(cooking)
    # test_all_recipe_scores(cooking)
    # test_one_recipe_score(cooking)
    # test_alternative_and_extra(cooking)
    # test_get_top_recipe(cooking)
    # test_get_top_recipe_no_ingredients(cooking)
    # test_chef_to_dict(cooking)
    # test_ingredient_images(cooking)
    # test_mongo(cooking)
    # debug_get_random_ingredient(cooking)
