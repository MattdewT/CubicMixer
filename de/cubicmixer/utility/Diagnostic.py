

# ---------------------------------------------------- custom error ----------------------------------------------------


class FileError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RecipeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidSyntax(Exception):

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return repr(self.position)


# ---------------------------------------------------- messages and color strings for terminal -------------------------


class bcolors:
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