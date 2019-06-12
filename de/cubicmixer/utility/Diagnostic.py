
'''
Diagnostics provides customs errors, often used debug string and color strings. It also keeps track of the loading and
parsing progress and success of scripts.
'''


# ---------------------------------------------------- custom error ----------------------------------------------------


class FileError(Exception):

    '''
    This error raises, when the script type cant be defined as ingredient or recipe (is or rs in script)
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RecipeError(Exception):

    '''
    This error raises, when the recipe has no syntax errors, but has semantics errors. These is often caused, by typos
    or not loaded ingredients.
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidSyntax(Exception):

    '''
    This errors raises, when the syntax is invalid.
    '''

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return repr(self.position)


# ---------------------------------------------------- messages and color strings for terminal -------------------------


class bcolors:

    '''
    Standard ansi color strings, to simplify debug messaging.
    '''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


debug_str = bcolors.OKBLUE + "[Debug]: "
error_str = bcolors.FAIL + "[Error]: "
warning_str = bcolors.WARNING + "[Warning]: "

display_str = bcolors.BOLD + "[Display]: "


separator_str = "-------------------------------------------------------------------------------------------------"


# ---------------------------------------------------- debug variables -------------------------------------------------


discarded_recipe = 0
discarded_ingredients = 0
unloaded_scripts = 0

loaded_scripts = 0
