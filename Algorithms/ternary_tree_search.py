import numpy as np
from ternary_tree import TernaryTree

"""
In this assignment, you have write a recursive function to search a value in a Ternary Tree, see ternary_tree.py.
A ternary tree is a tree where each node can have 3 children instead of 2 with a Binary Tree.

Hint: You can find an image in the template how a ternary tree could look like.
"""

def search(tree, value):
    """
    This method search for a node with the value "value".
    If the node is not found it returns None.

    :param value: The value that is search for.
    :type value: int
    :return: This returns the node or None
    :rtype: Node
    """
    return recursive_search(tree.root, value)

def recursive_search(current_node, value):
    """
    This is a recursive helper function for "search".
    This makes it possible to do the exhaustive search.

    :param value: The value that is search for.
    :type value: int
    :param current_node: The current node in the Ternary tree.
    :type current_node: Node
    :return: This returns the node
    :rtype: Node
    """
    if current_node is None:
        return None
    if current_node.info == value:
        return current_node

    found_node = recursive_search(current_node.left, value)
    if found_node is not None:
        return found_node

    found_node = recursive_search(current_node.middle, value)
    if found_node is not None:
        return found_node

    return recursive_search(current_node.right, value)

if __name__ == "__main__":
    RNG = np.random.default_rng()
    size = 50
    tree = TernaryTree()

    store_values = []
    for value in RNG.integers(0, size*4, size):
        tree.add(value)
        store_values.append(value)

    print(f"The current values in the tree: {store_values}")
    for _ in range(3):
        print(f"Is the value {(search_value := RNG.choice(store_values))} in the tree? according to your tree: {search(tree, search_value) is not None}, correct answer: True")
    for search_value in RNG.integers(0, size*4, 3):
        print(f"Is the value {search_value} in the tree? according to your tree: {search(tree, search_value) is not None}, correct answer: {search_value in store_values}")
