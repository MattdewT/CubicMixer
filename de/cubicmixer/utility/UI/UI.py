"""
UI Prototyping

Setup           Menumode                long
                                        short
                Operationmode           recipe mode
                                        random mode
Info            Loaded Scripts Infos    loaded scripts
                                        loaded recipes
                                        loaded ingredients
                (Discarded Inforamtion) discarded scripts
                                        discarded recipes
                                        discarded ingredients
                Version                 version xx
                Developer               Mathdew
                                        Timdew
                Help                    Github: MattdewT/CubicMixer
(Maintenance)   test Valves             chose valve by                  ingredient
                                                                        position
                reboot
Dice            Connection Status       Connection_Status
                                        ping
                Idle Counter            idle_counter_time
Chose Drink

BootUp
Spalsh Screen
Script Information
Dice Status

Mixing Loop
    Dice Input Information
    Displaying Result
    Mixing (with progress bar?)
"""

from Tree import Tree, LeafNode, Node


class UserInterface:

    def __init__(self):
        self.UITree = Tree()
        self.setup_tree()
        self.current_position = 0

    def switch_left(self):
        self.current_position += 1
        if self.current_position >= len(self.UITree.current_node.child_list):
            self.current_position = 0

    def switch_right(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = len(self.UITree.current_node.child_list) - 1

    def enter(self):
        self.UITree.descend(self.current_position)

    def back(self):
        self.UITree.ascend()

    def setup_tree(self):
        self.UITree.add_node(Node("Setup", False))

        self.UITree.descend(0)
        self.UITree.add_node(Node("Menumode", False))

        self.UITree.descend(0)
        self.UITree.add_node(LeafNode("True", True))
        self.UITree.add_node(LeafNode("False", False))

        self.UITree.ascend()
        self.UITree.add_node(Node("Operationmode", False))

        self.UITree.ascend()
        self.UITree.add_node(Node("Info", False))
        self.UITree.add_node(Node("Maintenance", True))
        self.UITree.add_node(Node("Dice", False))
        self.UITree.add_node(Node("Chose Drink", False))


class UIMessage:

    def __init__(self):
        self.msg


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
