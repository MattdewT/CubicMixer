import EBNF
from Library import automat_scripts, library, Recipe
from utility.Diagnostic import FileError, InvalidSyntax, RecipeError
from utility import Diagnostic

is_list = []
rs_list = []


"""
The FileIO module handles the loading and parsing of ingredient and recipes scripts.
"""

# ------------------------------------------------- script loading -----------------------------------------------------


def load_script(script_path):
    """
    Loads up script and makes a quick syntax check with the automat.
    :param script_path: full absolute path to the script
    """
    print Diagnostic.separator_str
    print Diagnostic.debug_str + "Loading Script:" + script_path + Diagnostic.bcolors.ENDC      # debug messaging

    lines_str = "Error occur during loading"                                                    # default string

    try:
        file_object = open(script_path, "r")
        lines_list = file_object.readlines()
        file_object.close()                                                                     # load script

        lines_str = ''.join(lines_list)                                                         # make a single line out of the list

        EBNF.check_syntax(lines_str, automat_scripts)

        sort_script_type(lines_str, script_path)

        Diagnostic.loaded_scripts += 1                                                          # count loaded scripts

    except IOError:
        print Diagnostic.error_str + "Problems with File loading: ", script_path + Diagnostic.bcolors.ENDC
        Diagnostic.unloaded_scripts += 1
    except InvalidSyntax as e:
        print Diagnostic.error_str + "SyntaxError, discarding Script, Error in:", describe_syntax_error(e.position, lines_str, script_path) + Diagnostic.bcolors.ENDC
        Diagnostic.unloaded_scripts += 1
    except FileError:
        print Diagnostic.error_str + "Error parsing filetype, please check first line of script: ", script_path + Diagnostic.bcolors.ENDC
        Diagnostic.unloaded_scripts += 1


def sort_script_type(lines_str, script_path):
    """
    Sorts the script by script type and saves them accordingly in their list.
    :param lines_str: loaded script as a single string with \n as line separators
    :param script_path: absolute path to the script
    .:raises FileError, wrong script type
    """
    file_type = lines_str.split('\n')[0]                                        # fetch first line of the script with script type information

    if file_type == "rs":                                                       # if it is a recipe script
        rs_list.append(lines_str)
    elif file_type == "is":                                                     # if it is a ingredient script
        is_list.append(lines_str)
    else:
        raise FileError(["wrong file type", script_path])


# ------------------------------------------------- script parsing -----------------------------------------------------


def parse_ingredient_dict():
    """
    Parses the ingredient scripts and saves them in the database
    """
    for ingredients_scripts in is_list:
        split_lines = ingredients_scripts.split('\n')
        for l in split_lines:
            args = l.split(" ")
            if len(args) > 1:                                            # make sure there is a complete line to parse
                library.add_ingredient([args[0], int(args[2])])          # line looks like this "Banane Ventil 12"


def parse_recipes_list():
    """
    Parses the recipes scripts and saves them in the database
    """
    for recipes_scripts in rs_list:
        split_lines = recipes_scripts.split('\n')

        recipe = Recipe()

        recipe_flawless = True                                                  # only flawless recipes can be added
        recipe_ingredient_added = False                                         # make sure no empty recipes get added
        enter_counter = 0                                                       # variables for detecting recipe end
        line_counter = 0                                                        # variables for detecting recipe end

        for l in split_lines:
            line_counter += 1
            args = l.split(" ")
            if (len(args) == 1) and (l != "rs") and (l != ""):                  # excluding scripttype and blank lines
                recipe.set_name(l)
            elif len(args) == 2:                                                # parsing ingredients for format '50ml'
                recipe_flawless &= parse_recipe_ingredient([args[0], float(args[1].strip("ml"))], recipe)
                recipe_ingredient_added = True
            elif len(args) == 3:                                                # parsing ingredients for format '50 ml'
                recipe_flawless &= parse_recipe_ingredient([args[0], float(args[1])], recipe)
                recipe_ingredient_added = True
            else:
                if recipe_ingredient_added:
                    enter_counter += 1

            if enter_counter >= 1 or line_counter == len(split_lines):          # if one or more lines ar empty, the recipes has ended, alternatively if there are no more chars left
                if recipe_flawless:                                             # only recipes with no errors get loaded in the database
                    library.add_recipe(recipe)

                enter_counter = 0                                               # reset variables for the next recipe
                recipe_ingredient_added = False
                recipe = Recipe()
                recipe_flawless = True


def parse_recipe_ingredient(args, recipe):
    """
    Adds ingredient to  a recipe and checks for errors in the ingredient.
    :param args: ingredient to add
    :param recipe: recipe object
    :return: if the ingredient was added successfully
    """
    try:
        recipe.add_ingredient(args)
        return True
    except RecipeError as e:
        print Diagnostic.warning_str + e.value + ", discarding recipe '" + recipe.name + "'" + Diagnostic.bcolors.ENDC
        Diagnostic.discarded_recipe += 1
        return False

# ------------------------------------------------- error decoding -----------------------------------------------------


def describe_syntax_error(error_position, string, path):
    """
    Converts the relative error position from the single line string to understandable line and character format.
    :param error_position: integer number, with the position of the invalid char in single line string
    :param string: loaded script as single string with \n as line separators
    :param path: absolute path to the script
    :return:
    """
    if error_position >= 0:
        line = 1                            # line in that the error occurred
        line_position = 1                   # character which caused the error
        for i in range(error_position):
            line_position += 1
            if string[i] == '\n':
                line += 1
                line_position = 1

        return " Line: " + str(line) + " Character: " + str(line_position) + " - Path: " + path

    else:
        return " Script uncompleted - Path: " + path
