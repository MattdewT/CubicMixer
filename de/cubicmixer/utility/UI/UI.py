from Tree import Tree, LeafNode, Node
import hardware
import scripts
from utility import Diagnostic
from Dice import DiceData
import time

"""
UI defines the complete user interface, from the menu tree, that can be accessed by the buttons, or the button handling
itself. 
"""


class UserInterface:

    """
    UserInterface holds the menu tree and all tree interactions.
    """

    def __init__(self, config):
        """
        :param config: Config object with all options and menu callback functions.
        """
        self.config = config
        self.UITree = Tree()
        self.setup_tree()
        self.current_position = 0

    def switch_left(self):
        """
        Switch to the next child node on the left side of the current active node.
        """
        self.current_position += 1
        if self.current_position >= len(self.UITree.current_node.parent_node.get_children()):                   # detect overflow
            self.current_position = 0                                                                           # start child list from beginning
        self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]   # set child to the left as the next active node

        if isinstance(self.UITree.current_node, Node):                                                          # checks if the current node is no leave node, because leaf nodes cant be hidden
            if self.UITree.current_node.is_hidden and not self.config.menu_long:                                # skip hidden nodes
                self.current_position += 1
                if self.current_position >= len(self.UITree.current_node.parent_node.get_children()):           # detect overflow
                    self.current_position = 0                                                                   # start child list from beginning
                self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]      # set child to the left as the next active node

        self.update_display()

    def switch_right(self):
        """
        Switch to the next child node on the right side of the current active node.
        """
        self.current_position -= 1
        if self.current_position < 0:                                                                           # detect overflow
            self.current_position = len(self.UITree.current_node.parent_node.get_children()) - 1                # start list from the end
        self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]   # set child to the right as the next active node

        if isinstance(self.UITree.current_node, Node):                                                          # checks if the current node is no leave node, because leaf nodes cant be hidden
            if self.UITree.current_node.is_hidden and not self.config.menu_long:                                # skip hidden nodes
                self.current_position -= 1
                if self.current_position < 0:                                                                   # detect overflow
                    self.current_position = len(self.UITree.current_node.parent_node.get_children()) - 1        # start list from the end
                self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]       # set child to the left as the next active node

        self.update_display()

    def enter(self):
        """
        Descend to currently pointed node. If the currently pointed node is a leaf node, the on_enter() functions get called.
        """
        is_leaf_node = True if isinstance(self.UITree.current_node, LeafNode) else False
        self.current_position = 0
        self.UITree.descend(self.current_position)
        if not is_leaf_node:
            self.update_display()

    def back(self):
        """
        Ascend in tree one layer higher.
        """
        self.UITree.ascend()
        self.update_display()

    def update_display(self):
        """
        If the something about the currently pointed node or active node had changed, this function need s to be called.
        It updates the lcd with current active node message.
        """
        hardware.Display.write_display(self.UITree.current_node.msg)

    def setup_tree(self):
        """
        Setups the menu tree with all entries. To see an ascii print out of menu structure, you can look at the console
        output or  call self.UITree.print(). An example print out looks like following, notice that the 'test valves',
        'loaded scripts information' and the 'chose drink' paragraphs may alter, because they are depending on
        the loaded scripts.


        Root
        ----Setup
        --------Menumode
        ------------True
        ------------False
        --------Operationmode
        ------------Recipe
        ------------Ingredient
        ----Info
        --------Loaded Script
        --------Information
        ------------6
                    Script(s) loaded
        ------------2
                    Recipe(s) loaded
        ------------3
                    Ingredient(s) loaded
        --------(Discarded Information)
        ------------1
                    Discarded Scripts
        ------------2
                    Discarded Recipes
        ------------1
                    Discarded Ingredients
        --------Version
        ------------version 4.2
        --------Developer
        ------------MathDew
        ------------TimDew
        --------Help
        ------------Github
                    Repository
        ----(Maintenance)
        --------reboot
        --------test valves
        ------------chose by
        ------------ingredient
        ----------------Blau
        ----------------Gelb
        ----------------Rot
        ------------chose by
        ------------position
        ----------------1
        ----------------2
        ----------------3
        ----------------4
        ----Chose Drink
        --------calibrate
        --------Bunt

        """
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

        self.UITree.add_node(Node(["Loaded Script", "Information"], False))								# Initialising Submenu Loaded Script Information

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode([str(Diagnostic.loaded_scripts), "Script(s) loaded"], self.config.nothing))					# LSI Loaded Scripts
        self.UITree.add_node(LeafNode([str(len(scripts.library.recipes_list)), "Recipe(s) loaded"],  self.config.nothing))			# LSI Loaded Recipes
        self.UITree.add_node(LeafNode([str(len(scripts.library.ingredients_dict)), "Ingredient(s) loaded"],  self.config.nothing))	# LSI Loaded Ingredients

        self.UITree.ascend()
        self.UITree.add_node(Node(["Discarded Information", ""], True))                                 # Initialising Submenu Discarded Information

        self.UITree.descend(1)

        self.UITree.add_node(LeafNode([str(Diagnostic.unloaded_scripts), "Discarded Scripts"], self.config.nothing))				# DI Discarded Scripts
        self.UITree.add_node(LeafNode([str(Diagnostic.discarded_recipe), "Discarded Recipes"], self.config.nothing))				# DI Discarded Recipes
        self.UITree.add_node(LeafNode([str(Diagnostic.discarded_ingredients), "Discarded Ingredients"], self.config.nothing))		# DI Discarded Ingredients

        self.UITree.ascend()
        self.UITree.add_node(Node(["Version", ""], False))                                              # Initialising Submenu Version

        self.UITree.descend(2)

        self.UITree.add_node(LeafNode(["version 4.2", ""], self.config.nothing))						# Version 4.2

        self.UITree.ascend()
        self.UITree.add_node(Node(["Developer", ""], False))                                            # Initialising Submenu Developer

        self.UITree.descend(3)

        self.UITree.add_node(LeafNode(["MathDew", ""], self.config.nothing))							# Developer MathDew
        self.UITree.add_node(LeafNode(["TimDew", ""], self.config.nothing))								# Developer Timdew

        self.UITree.ascend()
        self.UITree.add_node(Node(["Help", ""], False))                                                 # Initialising Submenu Help

        self.UITree.descend(4)

        self.UITree.add_node(LeafNode(["Github", "Repository"], self.config.display_msg, ["MattdewT", "CubicMixer"]))		# Help Github : MattdewT/Cubicmixer

        self.UITree.add_node_to_root(Node(["Maintenance", ""], True))                                   # Initialising Menu Maintenance
        self.UITree.go_to_root()
        self.UITree.descend(2)

        self.UITree.add_node(LeafNode(["shutdown", "script"], self.config.stop_program))								# Maintenance reboot
        self.UITree.add_node(Node(["test valves", ""], False))											# Initialising Submenu test valves

        self.UITree.descend(1)
        self.UITree.add_node(Node(["chose by", "ingredient"], False))									# tv chose by ingredient
        self.UITree.add_node(Node(["chose by", "position"], False))										# tv chose by position

        self.UITree.descend(0)
        for ingredient in scripts.library.ingredients_dict:
            self.UITree.add_node(LeafNode([ingredient, ""], self.config.test_valve_by_ingredient, ingredient))      # all loaded ingredients

        self.UITree.ascend()
        self.UITree.descend(1)
        for position in self.config.ns.vc.valve_dict:
            self.UITree.add_node(LeafNode([str(position), ""], self.config.test_valve_by_position, position))       # add all connected valves

        self.UITree.add_node_to_root(Node(["Chose Drink", ""], False))									# Initialising Menu Chose Drink
        self.UITree.go_to_root()
        self.UITree.descend(3)
        for recipe in scripts.library.recipes_list:
            self.UITree.add_node(LeafNode([recipe.name, ""], self.config.mix_drink, recipe))            # add all loaded recipes


class Config:

    """
    Config contains many options and provides all callback functions for the leaf nodes in the menu tree.
    """

    def __init__(self, ns, library, mixer):
        """
        :param ns: shared namespace object
        :param library: library with all loaded recipes and ingredients
        :param mixer: mixer instance
        """
        self.menu_long = True                           # option: menu mode, full or hidden
        self.ns = ns
        self.ns.mix_by_recipes = True                   # option: operation mode, mix by recipe or mix by ingredient
        self.library = library
        self.mixer = mixer

    def set_menu_mode(self, args):
        """
        Sets the menu mode to hide advanced functions or display them.
        :param args: list with the parameters: [menu_long]
        """
        self.menu_long = args[0]
        print Diagnostic.debug_str + "set menu to detailed view: " + str(args[0]) + Diagnostic.bcolors.ENDC

    def set_operation_mode(self, args):
        """
        Sets the operation mode of the mixer: mix by random recipe or mix by multiple random ingredients
        :param args: list with the parameters: [mix_by_recipe]
        """
        self.ns.mix_by_recipes = args[0]
        print Diagnostic.debug_str + "set mixing mode by recipe: " + str(args[0]) + Diagnostic.bcolors.ENDC

    @staticmethod
    def display_msg(args):
        """
        Prints a simple message to the lcd.
        :param args: list with the parameters: [msg_to_display]
        """
        hardware.Display.write_display(args[0])

    def stop_program(self):
        print Diagnostic.debug_str + "Stopping program" + Diagnostic.bcolors.ENDC
        self.ns.running = False

    def test_valve_by_position(self, args):
        """
        Test the valve specified by valve position, by dispensing small amount of liquid.
        :param args: list with the parameters: [valve_position]
        """
        vc = self.ns.vc
        vc.open_valves({args[0]: 10})
        self.ns.vc = vc

    def test_valve_by_ingredient(self, args):
        """
        Test the valve specified by ingredient, by dispensing small amount of liquid.
        :param args: list with the parameters: [ingredient_key]
        """
        for valve in self.library.ingredients_dict[args[0]]:                # fetch all valves corresponding to the specified ingredient
            vc = self.ns.vc
            vc.open_valves({valve: 10})
            self.ns.vc = vc                                                 # update valve controller to the shared namespace

    def mix_drink(self, args):
        """
        Starts the mixing process for the chosen recipe.
        :param args: list with the parameters: [recipe_object]
        """
        vc = self.ns.vc
        vc.open_valves(self.mixer.mix_drink_recipe(args[0], self.library))
        self.ns.vc = vc                                                     # update valve controller to the shared namespace

    @staticmethod
    def nothing():
        """
        Placeholder function, that fills up leaf nodes, that are only needed for their display message.
        """
        pass


def update_keyboard(ui_interface, namespace):
    """
    Fetches and parses any input given by the keyboard.
    :param ui_interface: user interface object
    :param namespace: shared namespace object
    """
    def trigger_dice_loop(ns):
        """
        Simulates a dice movement to trigger the dice loop, so that can pick up the simulated dice throw result by the dice simulation
        :param ns: shared namespace object
        """
        ns.dice_data = DiceData([0, 0, 0], False)
        time.sleep(0.5)

    char = raw_input("input")
    if char == 'w':
        namespace.em.handle_event_button_pressed(namespace, ui_interface, hardware.IO.pin_enter)        # simulate enter button press
    elif char == 'a':
        namespace.em.handle_event_button_pressed(namespace, ui_interface, hardware.IO.pin_left)         # simulate left button press
    elif char == 's':
        namespace.em.handle_event_button_pressed(namespace, ui_interface, hardware.IO.pin_back)         # simulate back button press
    elif char == 'd':
        namespace.em.handle_event_button_pressed(namespace, ui_interface, hardware.IO.pin_right)        # simulate right button press
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
            " or 1 to 6 to emulate dice input" if namespace.emulate_dice else ""                        # give instructions when a non parse able input get received


def update_buttons(ui_interface, channel):
    """
    Translates the button presses to navigation in the menu tree.
    :param ui_interface: user interface object
    :param channel: GPIO interrupt channel
    """
    if channel == hardware.IO.pin_enter:
        ui_interface.enter()
    elif channel == hardware.IO.pin_left:
        ui_interface.switch_left()
    elif channel == hardware.IO.pin_back:
        ui_interface.back()
    elif channel == hardware.IO.pin_right:
        ui_interface.switch_right()
    else:
        print "Error parsing button input"
