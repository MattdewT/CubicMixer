class Tree:

    def __init__(self):                                                                                         # Creating BaseNode
        self.root = Node(["Root", ""], False)
        self.current_node = self.root

    def add_node(self, node):                                                                                   # Adding new Node to current Node   
        self.current_node.add_child(node)

    def add_node_to_root(self, node):                                                                           # Adding new Node to BaseNode   
        self.root.add_child(node)

    def descend(self, child_position):                                                                          # Go down one step of Nodes
        if isinstance(self.current_node, LeafNode):
            self.current_node.on_enter()
        else:
            self.current_node = self.current_node.get_children()[child_position]

    def ascend(self):                                                                                           # Go up one step of Nodes
        if self.current_node.parent_node.msg[0] != "Root":
            self.current_node = self.current_node.parent_node

    def print_tree(self):                                                                                       # Print current Node    
        self.root.print_node(0)

    def go_to_root(self):                                                                                       # Jump to specific Node    
        self.current_node = self.root


class Node:

    def __init__(self, msg, hidden):
        self.child_list = []
        self.parent_node = None
        self.msg = msg
        self.is_hidden = hidden

    def add_child(self, child_node):
        child_node.parent_node = self
        self.child_list.append(child_node)

    def get_message(self):
        return self.msg

    def get_children(self):
        return self.child_list

    def print_node(self, depth):
        print depth * 4 * "-" + ("(" if self.is_hidden else "") + self.msg[0] + (")" if self.is_hidden else "")
        if not self.msg[1] == "":
            print depth * 4 * "-" + ("(" if self.is_hidden else "") + self.msg[1] + (")" if self.is_hidden else "")
        for child in self.child_list:
            child.print_node(depth + 1)


class LeafNode:

    def __init__(self, msg, enter_function, *args):
        self.msg = msg
        self.enter_function = enter_function
        self.args = False
        if args:
            self.args = args

    def print_node(self, depth):
        print depth * 4 * "-" + self.msg[0]
        if not self.msg[1] == "":
            print depth * 4 * " " + self.msg[1]

    def on_enter(self):
        if self.args:
            self.enter_function(self.args)
        else:
            self.enter_function()

