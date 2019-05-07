import EBNF
from Library import automat_scripts, library, Recipe
from utility.Diagnostic import FileError, InvalidSyntax, RecipeError
from utility import Diagnostic

is_list = []
rs_list = []


# ------------------------------------------------- script loading -----------------------------------------------------


def load_script(script_path):
    print Diagnostic.separator_str
    print Diagnostic.debug_str + "Loading Script:" + script_path + Diagnostic.bcolors.ENDC

    lines_str = "Error occur during loading"

    try:
        file_object = open(script_path, "r")
        lines_list = file_object.readlines()
        file_object.close()

        lines_str = ''.join(lines_list)

        EBNF.check_syntax(lines_str, automat_scripts)

        sort_script_type(lines_str, script_path)

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
    file_type = lines_str.split('\n')[0]

    if file_type == "rs":
        rs_list.append(lines_str)
    elif file_type == "is":
        is_list.append(lines_str)
    else:
        raise FileError(["wrong file type", script_path])


# ------------------------------------------------- script parsing -----------------------------------------------------


def parse_ingredient_dict():
    for ingredients_scripts in is_list:
        split_lines = ingredients_scripts.split('\n')
        for l in split_lines:
            args = l.split(" ")
            if len(args) > 1:
                library.add_ingredient([args[0], int(args[2])])          # line looks like this "Banane Ventil 12"


def parse_recipes_list():
    for recipes_scripts in rs_list:
        split_lines = recipes_scripts.split('\n')

        recipe = Recipe()

        recipe_flawless = True
        recipe_ingredient_added = False
        enter_counter = 0
        line_counter = 0

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

            if enter_counter >= 1 or line_counter == len(split_lines):
                if recipe_flawless:
                    library.add_recipe(recipe)

                enter_counter = 0
                recipe_ingredient_added = False
                recipe = Recipe()
                recipe_flawless = True


def parse_recipe_ingredient(args, recipe):
    try:
        recipe.add_ingredient(args)
        return True
    except RecipeError as e:
        print Diagnostic.warning_str + e.value + ", discarding recipe '" + recipe.name + "'" + Diagnostic.bcolors.ENDC
        Diagnostic.discarded_recipe += 1
        return False

# ------------------------------------------------- error decoding -----------------------------------------------------


def describe_syntax_error(error_position, string, path):
    if error_position >= 0:
        line = 1
        line_position = 1
        for i in range(error_position):
            line_position += 1
            if string[i] == '\n':
                line += 1
                line_position = 1

        return " Line: " + str(line) + " Character: " + str(line_position) + " - Path: " + path

    else:
        return " Script uncompleted - Path: " + path
