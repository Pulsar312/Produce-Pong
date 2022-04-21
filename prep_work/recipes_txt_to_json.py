import json

# This is a file for converting the recipes we collected into a json format; only need to use this if recipes.txt is updated.

rows_per_recipe = 4


def read_txt_file(filename):
    content = open(filename, 'r').read().split('\n')
    all_recipes = []
    i = 0
    while i < len(content):

        recipe = {}
        for j in range(0, rows_per_recipe):
            (key, value) = content[i + j].lower().split(":")

            key = key.strip().replace(" ", "_")
            value = value.strip().split(",")

            if key == "recipe_name":
                value_split = value[0].split(" ")
                value = ""
                for name in range(0, len(value_split)):
                    value += value_split[name][0].upper() + value_split[name][1:] + " "
                value = value.strip()
            else:
                for ingredient in range(0, len(value)):
                    value[ingredient] = value[ingredient].strip()
                    if value[ingredient] == "":
                        value.remove("")
                if key == "alternative_ingredients":
                    for ingredient in range(0, len(value)):
                        substitution = value[ingredient][:value[ingredient].find("(")]
                        substituted = value[ingredient][value[ingredient].find("(") + 1: value[ingredient].find(")")]
                        value[ingredient] = [substituted.strip(), substitution.strip()]

            recipe[key] = value

        all_recipes.append(recipe)
        i += rows_per_recipe + 1  # plus 1 because empty line
    return all_recipes


if __name__ == '__main__':
    filename = 'recipes.txt'
    all_recipes = read_txt_file(filename)
    with open('recipes.json', 'w') as writeFile:
        writeFile.write(json.dumps(all_recipes))
    json.dumps(all_recipes)
