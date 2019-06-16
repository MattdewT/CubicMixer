import EBNF
from utility.Diagnostic import RecipeError
from utility import Diagnostic

"""
The Library module defines the project database and the recipe class. It also features some last checks before any
ingredient or recipe gets added.
"""


class Library:

    """
    The library holds all loaded scripts and forms the database for the complete project.
    """

    def __init__(self):
        self.ingredients_dict = {}
        self.recipes_list = []

    def add_recipe(self, entry):
        """
        Adds the recipe to the database, when enough space is available.
        :param entry: recipe object to add
        """
        if check_recipe_volume(entry):
            if len(self.recipes_list) >= max_recipe_quantity:                   # check for space
                print Diagnostic.error_str + "Quantity of recipes higher than " + str(max_recipe_quantity) + ", discarding recipe '" + entry.name + "'" + Diagnostic.bcolors.ENDC      # checking for max amount of loaded recipes
                Diagnostic.discarded_recipe += 1
            else:                                                               # add recipe
                self.recipes_list.append(entry)
                print Diagnostic.debug_str + "recipe added: " + entry.name + Diagnostic.bcolors.ENDC

    def add_ingredient(self, entry):
        """
        Adds ingredient to database, if there is enough space available and detects double entries and multiple uses of
        the same valve.
        :param entry: recipe to add
        """
        if entry[1]in [x for v in self.ingredients_dict.values() for x in v]:
            print Diagnostic.error_str + "Valve '" + str(entry[1]) + "' used multiple times, discarding ingredient '" + entry[0] + "'" + Diagnostic.bcolors.ENDC       # checking for double entrys for the valves
            Diagnostic.discarded_ingredients += 1
        elif len(self.ingredients_dict) >= max_ingredient_quantity:
            print Diagnostic.error_str + "Quantity of ingredients higher than " + str(max_ingredient_quantity) + ", discarding ingredient '" + entry[0] + "'" + Diagnostic.bcolors.ENDC      # checking for max amount of loaded ingredients
            Diagnostic.discarded_ingredients += 1
        elif entry[0] in self.ingredients_dict:
            print Diagnostic.warning_str + "Ingredient '" + entry[0] + "' already loaded" + Diagnostic.bcolors.ENDC             # checking for double entrys of the ingredients
            self.ingredients_dict[entry[0]].append(entry[1])
        else:
            self.ingredients_dict[entry[0]] = [entry[1]]

    def get_recipe_by_position(self, position):
        """
        Getter for recipe database
        :param position: position in the database
        :return: recipe object
        """
        return self.recipes_list[position]


def check_recipe_volume(recipe):
    """
    Checks the total volume and makes sure it is less than the max_cup_volume
    :param recipe: recipe to check
    :return: True, if the toatal volume is less then the max allowed volume.
    """
    total_volume = 0
    for ingredient in recipe.ingredients:
        total_volume += ingredient[1]

    if total_volume > max_cup_volume:
        print Diagnostic.error_str + "Total volume of recipe '" + recipe.name + "' larger than " + str(max_cup_volume) + "ml, discarding recipe" + Diagnostic.bcolors.ENDC
        Diagnostic.discarded_recipe += 1
        return False
    elif total_volume < min_cup_volume:                 # warning about to small recipes
        print Diagnostic.warning_str + "Total volume of recipe '" + recipe.name + "' smaller than " + str(min_cup_volume) + "ml" + Diagnostic.bcolors.ENDC
        return True
    else:
        return True


class Recipe:

    """
    Recipe defines a simple recipe, with a name, ingredient list and accordingly volumes.
    """

    def __init__(self):
        self.ingredients = []
        self.name = ""

    def set_name(self, name):
        """
        Setter for recipe name
        :param name: new name of the recipe
        """
        self.name = name

    def add_ingredient(self, ingredient):   # expects input list as following  [ingredient (String), volume (float)]
        """
        Adds ingredient to the recipe, if its available, else it discards the recipe.
        :param ingredient:
        :raises Recipe error when the ingredient is not loaded
        """
        if ingredient[0] in library.ingredients_dict:
            self.ingredients.append(ingredient)
        else:
            raise RecipeError("Ingredient '" + ingredient[0] + "' not yet loaded or isn't available")

    def clear(self):
        self.ingredients = []
        self.name = ""

    def __repr__(self):
        return self.name + str(self.ingredients)

# ----------------------------------------------------------- constants and variables ----------------------------------


library = Library()                                                             # global variable
automat_scripts = EBNF.setup_automat()                                          # global automat for script syntax checking

max_cup_volume = 300
min_cup_volume = 100

max_ingredient_quantity = 100                                                   # freely chosen values, manly duo the limitation of th display
max_recipe_quantity = 100

