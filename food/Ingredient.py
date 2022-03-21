from food import Recipe


class Ingredient:
    def __init__(self, name: str):
        self.name = name
        self.recipes = []

    def add_recipes(self, recipe: Recipe):
        if( recipe not in self.recipes):
            self.recipes.append(recipe)

    #method prints out all ingredients with the recipes
    def to_string(self):
        str = "Name: " + self.name
        str += "\t\t\t\t\t"
        str += "Recipes: ["
        for r in self.recipes:
            str += r.name + ", "
        str = str[:len(str) - 2] + "]"
        return str
