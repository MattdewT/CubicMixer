class Tree:

    def __init__(self):
        self.root = Node("Root", False)
        self.current_node = self.root

    def add_node(self, node):
        self.current_node.add_child(node)

    def descend(self, child_position):
        self.current_node = self.current_node.get_children()[child_position]

    def ascend(self):
        self.current_node = self.current_node.parent_node


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


class LeafNode:

    def __init__(self, msg, return_value):
        self.msg = msg
        self.return_value = return_value

