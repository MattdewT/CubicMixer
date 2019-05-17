"""
UI Prototyping

Setup           Menumode                long
                                        short
                Operationmode           recipe mode
                                        ingredient mode
Info            Loaded Scripts Infos    loaded scripts
                                        loaded recipes
                                        loaded ingredients
                (Discarded Information) discarded scripts
                                        discarded recipes
                                        discarded ingredients
                Version                 version 4.2
                Developer               Mathdew
                                        Timdew
                Help                    Github: MattdewT/CubicMixer
(Maintenance)   test Valves             chose valve by                  ingredient
                                                                        position
                reboot
Dice            Connection Status       Connection_Status
                                        ping
Chose Drink
-------------------------------------------------------------
BootUp
Splash Screen
Script Information
Dice Status

Mixing Loop
    Dice Input Information
    Displaying Result
    Mixing (with progress bar!)
"""

from Tree import Tree, LeafNode, Node
import hardware
from utility import Diagnostic


class UserInterface:

    def __init__(self):
        self.config = Config()
        self.UITree = Tree()
        self.setup_tree()
        self.current_position = 0

    def switch_left(self):
        self.current_position += 1
        if self.current_position >= len(self.UITree.current_node.parent_node.get_children()):
            self.current_position = 0
        self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]

        if isinstance(self.UITree.current_node, Node):      # skip hidden nodes
            if self.UITree.current_node.is_hidden and not self.config.menu_long:
                self.current_position += 1
                if self.current_position >= len(self.UITree.current_node.parent_node.get_children()):
                    self.current_position = 0
                self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]

        self.update_display()

    def switch_right(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = len(self.UITree.current_node.parent_node.get_children()) - 1
        self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]

        if isinstance(self.UITree.current_node, Node):      # skip hidden nodes
            if self.UITree.current_node.is_hidden and not self.config.menu_long:
                self.current_position -= 1
                if self.current_position < 0:
                    self.current_position = len(self.UITree.current_node.parent_node.get_children()) - 1
                self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]

        self.update_display()

    def enter(self):                                                                                    # Action Enter
        self.current_position = 0
        self.UITree.descend(self.current_position)
        self.update_display()

    def back(self):                                                                                     # Action Back
        self.UITree.ascend()
        self.update_display()

    def update_display(self):
        hardware.Display.write_display(self.UITree.current_node.msg)

    def setup_tree(self):

        self.UITree.add_node_to_root(Node(["Setup", ""], False))                                        # Initialising Menu Setup 

        self.UITree.descend(0)
        self.UITree.add_node(Node(["Menumode", ""], False))                                             # Initialising Submenu Menumode

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["True", ""], self.config.set_menu_mode, True))                   # Menumode long
        self.UITree.add_node(LeafNode(["False", ""], self.config.set_menu_mode, False))                 # Menumode short

        self.UITree.ascend()
        self.UITree.add_node(Node(["Operationmode", ""], False))                                        # Initialising Submenu Operationmode

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Recipe", ""], self.config.set_operation_mode, True))            # Operationmode Recipe
        self.UITree.add_node(LeafNode(["Ingredient", ""], self.config.set_operation_mode, False))       # Operationmode Ingredient

        self.UITree.add_node_to_root(Node(["Info", ""], False))                                         # Initialising Menu Info
        self.UITree.go_to_root()
        self.UITree.descend(1)

        self.UITree.add_node(Node(["Loaded Script Information", ""], False))                            # Initialising Submenu Loaded Script Information

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Loaded Scipts", ""], self.config.stuff))                        # LSI Loaded Scripts
        self.UITree.add_node(LeafNode(["Loaded Recipes", ""], self.config.stuff))                       # LSI Loaded Recipes
        self.UITree.add_node(LeafNode(["Loaded Ingredients", ""], self.config.stuff))                   # LSI Loaded Ingredients

        self.UITree.ascend()
        self.UITree.add_node(Node(["Discarded Information", ""], True))                                 # Initialising Submenu Discarded Information

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Discarded Scripts", ""], self.config.stuff))                    # DI Discarded Scripts
        self.UITree.add_node(LeafNode(["Discarded Recipes", ""], self.config.stuff))                    # DI Discarded Recipes
        self.UITree.add_node(LeafNode(["Discarded Ingredients", ""], self.config.stuff))                # DI Discarded Ingredients

        self.UITree.ascend()
        self.UITree.add_node(Node(["Version", ""], False))                                              # Initialising Submenu Version

        self.UITree.descend(2)
        self.UITree.add_node(LeafNode(["version 4.2", ""], self.config.stuff))                          # Version version 4.2

        self.UITree.ascend()
        self.UITree.add_node(Node(["Developer", ""], False))                                            # Initialising Submenu Developer

        self.UITree.descend(3)
        self.UITree.add_node(LeafNode(["MathDew", ""], self.config.stuff))                              # Developer MathDew
        self.UITree.add_node(LeafNode(["TimDew", ""], self.config.stuff))                               # Developer TimDew

        self.UITree.ascend()
        self.UITree.add_node(Node(["Help", ""], False))                                                 # Initialising Submenu Help

        self.UITree.descend(4)
        self.UITree.add_node(LeafNode(["Github : MattdewT/CubicMixer", ""], self.config.stuff))         # Help Github : MattdewT/Cubicmixer

        self.UITree.add_node_to_root(Node(["Maintenance", ""], True))                                   # Initialising Menu Maintenance
        self.UITree.go_to_root()
        self.UITree.descend(2)

        self.UITree.add_node(LeafNode(["reboot", ""], self.config.stuff))                               # Maintenance reboot
        self.UITree.add_node(Node(["test valves", ""], False))                                          # Initialising Submenu test valves

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["chose by", "ingredient"], self.config.stuff))                   # tv chose by ingredient
        self.UITree.add_node(LeafNode(["chose by", "position"], self.config.stuff))                     # tv chose by position

        self.UITree.add_node_to_root(Node(["Dice", ""], False))                                         # Initialising Menu Dice
        self.UITree.go_to_root()
        self.UITree.descend(3)

        self.UITree.add_node(Node(["Connection", "Status"], False))                                     # Initialising Submenu Connection Status

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Status", ""], self.config.stuff))                               # CS Status
        self.UITree.add_node(LeafNode(["Ping", ""], self.config.stuff))                                 # CS Ping

        self.UITree.add_node_to_root(LeafNode(["Chose Drink", ""], self.config.stuff))                  # Initialising Menu Chose Drink


class Config:

    def __init__(self):
        self.menu_long = False
        self.mix_by_recipes = True

    @staticmethod
    def print_to_display(msg):
        hardware.Display.write_display(msg)

    def set_menu_mode(self, is_long):
        self.menu_long = is_long
        print Diagnostic.debug_str + "set menu to detailed view: " + str(is_long) + Diagnostic.bcolors.ENDC

    def set_operation_mode(self, by_recipe):
        self.mix_by_recipes = by_recipe
        print Diagnostic.debug_str + "set mixing mode by recipe: " + str(by_recipe) + Diagnostic.bcolors.ENDC

    @staticmethod
    def reboot():
        print Diagnostic.debug_str + "Rebooting" + Diagnostic.bcolors.ENDC

    @staticmethod
    def ping():
        print Diagnostic.debug_str + "Rebooting" + Diagnostic.bcolors.ENDC

    # ToDo: Remove function
    @staticmethod
    def stuff():
        print Diagnostic.error_str + "please change function" + Diagnostic.bcolors.ENDC
        hardware.Display.write_display(["not defined yet", "please fix"])


def update(ui_interface):
    char = raw_input("input")
    if char == 'w':
        ui_interface.enter()
    elif char == 'a':
        ui_interface.switch_left()
    elif char == 's':
        ui_interface.back()
    elif char == 'd':
        ui_interface.switch_right()
    else:
        print "Wrong Input, use w = Enter, s = back, a = left, d = right"

