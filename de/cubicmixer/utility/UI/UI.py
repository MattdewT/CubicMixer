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

    def switch_right(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = len(self.UITree.current_node.parent_node.get_children()) - 1
        self.UITree.current_node = self.UITree.current_node.parent_node.get_children()[self.current_position]

    def enter(self):
        self.UITree.descend(self.current_position)

    def back(self):
        self.UITree.ascend()

    def setup_tree(self):

        self.UITree.add_node_to_root(Node(["Setup", ""], False))

        self.UITree.descend(0)
        self.UITree.add_node(Node(["Menumode", ""], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["True", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["False", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Operationmode", ""], False))

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Recipe", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Ingredient", ""], self.config.stuff))

        self.UITree.add_node_to_root(Node(["Info", ""], False))
        self.UITree.go_to_root()
        self.UITree.descend(1)

        self.UITree.add_node(Node(["Loaded Script Information", ""], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Loaded Scipts", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Loaded Recipes", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Loaded Ingredients", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Discarded Information", ""], True))

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["Discarded Scripts", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Discarded Recipes", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["Discarded Ingredients", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Version", ""], True))

        self.UITree.descend(2)
        self.UITree.add_node(LeafNode(["version 4.2", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Developer", ""], True))

        self.UITree.descend(3)
        self.UITree.add_node(LeafNode(["MathDew", ""], self.config.stuff))
        self.UITree.add_node(LeafNode(["TimDew", ""], self.config.stuff))

        self.UITree.ascend()
        self.UITree.add_node(Node(["Help", ""], True))

        self.UITree.descend(4)
        self.UITree.add_node(LeafNode(["Github : MattdewT/CubicMixer", ""], self.config.stuff))

        self.UITree.add_node_to_root(Node(["Maintenance", ""], True))
        self.UITree.go_to_root()
        self.UITree.descend(2)

        self.UITree.add_node(LeafNode(["reboot", ""], self.config.stuff()))
        self.UITree.add_node(Node(["test valves", ""], False))

        self.UITree.descend(1)
        self.UITree.add_node(LeafNode(["chose by", "ingredient"], self.config.stuff()))
        self.UITree.add_node(LeafNode(["chose by", "position"], self.config.stuff()))

        self.UITree.add_node_to_root(Node(["Dice", ""], False))
        self.UITree.go_to_root()
        self.UITree.descend(3)

        self.UITree.add_node(Node(["Connection", "Status"], False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode(["Status", ""], self.config.stuff()))
        self.UITree.add_node(LeafNode(["Ping", ""], self.config.stuff()))

        self.UITree.add_node_to_root(LeafNode(["Chose Drink", ""], self.config.stuff()))


class Config:

    def __init__(self):
        pass

    def stuff(self):
        print "hello"


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

