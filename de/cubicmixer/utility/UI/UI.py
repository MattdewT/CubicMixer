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

    def handle_button(self):
        pass
