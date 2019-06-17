class Tree:

    def __init__(self):                                                                                         # Creating BaseNode
        self.root = Node(["Root", ""], False)
        self.current_node = self.root

    def add_node(self, node):                                                                                   # Adding new Node to current Node   
        """
        Adds give node as child to the current active node.
        :param node: Node to add to the current node
        """
        self.current_node.add_child(node)

    def add_node_to_root(self, node):                                                                           # Adding new Node to BaseNode   
        """
        Adds given node as child to the root node.
        :param node: Node to add to root
        """
        self.root.add_child(node)

    def descend(self, child_position):                                                                          # Go down one step of Nodes
        """
        Descend to a specified child. Calls the on enter functions, if it is a LeafNode.
        :param child_position: which child to ascend to
        """
        if isinstance(self.current_node, LeafNode):
            self.current_node.on_enter()
        else:
            self.current_node = self.current_node.get_children()[child_position]

    def ascend(self):                                                                                           # Go up one step of Nodes
        """
        Ascend to the parent node. Root node cant be accessed by this function
        """
        if self.current_node.parent_node.msg[0] != "Root":
            self.current_node = self.current_node.parent_node

    def print_tree(self):                                                                                       # Print current Node    
        """
        Prints an ascii diagram of the complete tree using recursion.
        """
        self.root.print_node(0)

    def go_to_root(self):                                                                                       # Jump to root Node
        """
        Go to root node.
        """
        self.current_node = self.root


class Node:

    def __init__(self, msg, hidden):
        """
        :param msg: Display message on the lcd, when it is the current active node
        :param hidden: if the node is hidden in the short menu
        """
        self.child_list = []
        self.parent_node = None
        self.msg = msg
        self.is_hidden = hidden

    def add_child(self, child_node):
        """
        Adds node as child to itself.
        :param child_node: child node to add
        """
        child_node.parent_node = self                       # sets parent node
        self.child_list.append(child_node)

    def get_message(self):
        """
        Getter for the Node message
        :return: dipaly message of the node
        """
        return self.msg

    def get_children(self):
        """
        Getter for the children list.
        :return: all children of the node as list
        """
        return self.child_list

    def print_node(self, depth):
        """
        Prints the content of the Node in a simple ascii tree diagram.
        :param depth: current depth of the tree
        """
        print depth * 4 * "-" + ("(" if self.is_hidden else "") + self.msg[0] + (")" if self.is_hidden else "")         # parenthese, if the node is hidden
        if not self.msg[1] == "":                                                                                       # skip second line, if its empty
            print depth * 4 * "-" + ("(" if self.is_hidden else "") + self.msg[1] + (")" if self.is_hidden else "")
        for child in self.child_list:                                                                                   # recursion call
            child.print_node(depth + 1)


class LeafNode:

    """
    LeafNode is the last entry in the tree. Each LeafNode holds a functions, that gets called, when ever the user
    descend on a LeafNode.
    """

    def __init__(self, msg, enter_function, *args):
        self.msg = msg
        self.enter_function = enter_function
        self.args_ = False
        if args:
            self.args = args

    def print_node(self, depth):
        """
        Prints the content of the LeafNode in a simple ascii tree diagram.
        :param depth: current depth of the tree
        """
        print depth * 4 * "-" + self.msg[0]
        if not self.msg[1] == "":                               # skip second line, if it is empty
            print depth * 4 * " " + self.msg[1]

    def on_enter(self):
        """
        Call function on enter press.
        """
        if self.args_:                                          # pass arguments
            self.enter_function(self.args)
        else:
            self.enter_function()

