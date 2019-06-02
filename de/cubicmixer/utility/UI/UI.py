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
import scripts
from utility import Diagnostic
from Dice import DiceData
import time


class UserInterface:

    def __init__(self, config):
        self.config = config
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

    def enter(self):
        is_leaf_node = True if isinstance(self.UITree.current_node, LeafNode) else False
        self.current_position = 0
        self.UITree.descend(self.current_position)
        if not is_leaf_node:
            self.update_display()

    def back(self):
        self.UITree.ascend()
        self.update_display()

    def update_display(self):
        hardware.Display.write_display(self.UITree.current_node.msg)

    def setup_tree(self):

        self.UITree.add_node_to_root(Node(["Setup", ""], False))

        self.UITree.descend(0)
        self.UITree.add_node(Node(["Menumode", ""], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["True", ""], self.config.set_menu_mode, True))
        self.UITree.add_node(LeafNode(["False", ""], self.config.set_menu_mode, False))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Operationmode", ""], False))

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Recipe", ""], self.config.set_operation_mode, True))
        self.UITree.add_node(LeafNode(["Ingredient", ""], self.config.set_operation_mode, False))

        self.UITree.add_node_to_root(Node(["Info", ""], False))
        self.UITree.go_to_root()
        self.UITree.descend(1)

        self.UITree.add_node(Node(["Loaded Script", "Information"], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Loaded Scipts", ""], self.config.display_msg, [str(Diagnostic.loaded_scripts), "Scripts loaded"]))
        self.UITree.add_node(LeafNode(["Loaded Recipes", ""],  self.config.display_msg, [str(len(scripts.library.recipes_list)), "Recipes loaded"]))
        self.UITree.add_node(LeafNode(["Loaded Ingredients", ""],  self.config.display_msg, [str(len(scripts.library.ingredients_dict)), "Ingredients loaded"]))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Discarded Information", ""], True))

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Discarded Scripts", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Discarded Recipes", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Discarded Ingredients", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Version", ""], False))

        self.UITree.descend(2)
        self.UITree.add_node(LeafNode(["version 4.2", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Developer", ""], False))

        self.UITree.descend(3)
        self.UITree.add_node(LeafNode(["MathDew", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["TimDew", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Help", ""], False))

        self.UITree.descend(4)
        self.UITree.add_node(LeafNode(["Github:", "MattdewT/CubicMixer"], self.config.stuff))

        self.UITree.add_node_to_root(Node(["Maintenance", ""], True))
        self.UITree.go_to_root()
        self.UITree.descend(2)

        self.UITree.add_node(LeafNode(["reboot", ""], self.config.reboot))
        self.UITree.add_node(Node(["test valves", ""], False))

        self.UITree.descend(1)
        self.UITree.add_node(Node(["chose by", "ingredient"], False))
        self.UITree.add_node(Node(["chose by", "position"], False))

        self.UITree.descend(0)
        for ingredient in scripts.library.ingredients_dict:
            self.UITree.add_node(LeafNode([ingredient, ""], self.config.test_valve_by_ingredient, ingredient))

        self.UITree.ascend()
        self.UITree.descend(1)
        for position in hardware.ValveMaster.vc.valve_dict:
            self.UITree.add_node(LeafNode([str(position), ""], self.config.test_valve_by_position, position))

        self.UITree.add_node_to_root(Node(["Dice", ""], False))
        self.UITree.go_to_root()
        self.UITree.descend(3)

        self.UITree.add_node(Node(["Connection", "Status"], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Status", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Ping", ""], self.config.stuff))

        self.UITree.add_node_to_root(Node(["Chose Drink", ""], False))
        self.UITree.go_to_root()
        self.UITree.descend(4)
        for recipe in scripts.library.recipes_list:
            self.UITree.add_node(LeafNode([recipe.name, ""], self.config.stuff))


class Config:

    def __init__(self, ns, valve_controller, library):
        self.menu_long = True
        self.ns = ns
        self.ns.mix_by_recipes = True
        self.library = library
        self.valve_controller = valve_controller

    @staticmethod
    def print_to_display(msg):
        hardware.Display.write_display(msg)

    def set_menu_mode(self, args):
        self.menu_long = args[0]
        print Diagnostic.debug_str + "set menu to detailed view: " + str(args[0]) + Diagnostic.bcolors.ENDC

    def set_operation_mode(self, args):
        self.ns.mix_by_recipes = args[0]
        print Diagnostic.debug_str + "set mixing mode by recipe: " + str(args[0]) + Diagnostic.bcolors.ENDC

    @staticmethod
    def display_msg(msg):
        hardware.Display.write_display(msg[0])

    def reboot(self):
        print Diagnostic.debug_str + "Rebooting" + Diagnostic.bcolors.ENDC
        self.ns.running = False

    @staticmethod
    def ping():
        print Diagnostic.debug_str + "Pinging" + Diagnostic.bcolors.ENDC

    def test_valve_by_position(self, args):
        self.valve_controller.open_valves({args[0]: 10})

    def test_valve_by_ingredient(self, args):
        for valve in self.library.ingredients_dict[args[0]]:
            self.valve_controller.open_valves({valve: 10})

    # ToDo: Remove function
    @staticmethod
    def stuff():
        print Diagnostic.error_str + "please change function" + Diagnostic.bcolors.ENDC
        hardware.Display.write_display(["not defined yet", "please fix"])


def update_keyboard(ui_interface, namespace):

    def trigger_dice_loop(ns):
        ns.dice_data = DiceData([0, 0, 0], False)
        time.sleep(0.5)

    char = raw_input("input")
    if char == 'w':
        ui_interface.enter()
    elif char == 'a':
        ui_interface.switch_left()
    elif char == 's':
        ui_interface.back()
    elif char == 'd':
        ui_interface.switch_right()
    elif char == '1' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([-1, 0, 0], True)
    elif char == '2' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([0, 0, -1], True)
    elif char == '3' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([0, -1, 0], True)
    elif char == '4' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([0, 1, 0], True)
    elif char == '5' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([0, 0, 1], True)
    elif char == '6' and namespace.emulate_dice:
        trigger_dice_loop(namespace)
        namespace.dice_data = DiceData([1, 0, 0], True)
    else:
        print "Wrong Input, use w = Enter, s = back, a = left, d = right", \
            " or 1 to 6 to emulate dice input" if namespace.emulate_dice else ""


def update_buttons(ui_interface, channel):
    if channel == 17:
        ui_interface.enter()
    elif channel == 18:
        ui_interface.switch_left()
    elif channel == 19:
        ui_interface.back()
    elif channel == 20:
        ui_interface.switch_right()
    else:
        print "Error parsing button input"
