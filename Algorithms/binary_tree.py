import numpy as np
import typing


class Node(object):

    def __init__(self, info, left, right):
        self.info = info
        self.left = left
        self.right = right


def visualize_tree(root: Node, depth: int=0, type : str = "Root") -> None:
    if root is None:
        return
    print('%s%s> %s' % ('--' * depth, type, root.info))
    if root.left is not None:
        visualize_tree(root.left, depth + 1, 'L')
    if root.right is not None:
        visualize_tree(root.right,  depth + 1, 'R')

def count_leafs(root: Node) -> int:
    """
    Counts the number of leafs in a binary tree. Recursive function.

    :param root: The root of the (sub)tree
    :return: the number of leafs
    """
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leafs(root.left) + count_leafs(root.right)



def get_height(root: Node) -> int:
    """
    Determines the height of a binary tree. Recursive function.

    :param root: The root of the (sub)tree
    :return: the height of the (sub)tree
    """
    if root is None:
        return -1
    left_height = get_height(root.left)
    right_height = get_height(root.right)

    return max(left_height, right_height) + 1


def get_highest_value(root: Node) -> int:
    """
    Gets the highest value out of a binary tree (not a binary search tree!!)
    Recursive function.

    :param root: The root of the (sub)tree
    :return: the highest value within this (sub)tree
    """
    if root is None:
        return 0
    left_val = get_highest_value(root.left)
    right_val = get_highest_value(root.right)

    return max(root.info, left_val, right_val)


def get_greatest_smaller_value(root: Node) -> Node:
    """
    Returns the node with the greatest value smaller than the root.
    You can assume that this is a binary search tree. Also, you can
    assume that this function will only be used if such smaller values
    exists. Hint: This function is not recursive. Think of the binary 
    search tree property

    :param root: The root of the (sub)tree
    :return: the Node with the greatest value smaller than the root
    """

    current = root.left
    while current.right is not None:
        current = current.right
    return current



def get_smallest_greater_value(root: Node) -> Node:
    """
    Returns the node with the smallest value greater than the root.
    You can assume that this is a binary search tree. Also, you can
    assume that this function will only be used if such greater values
    exists. Hint: This function is not recursive. Think of the binary 
    search tree property

    :param root: The root of the (sub)tree
    :return: the Node with the smallest value greater than the root
    """
    current = root.right
    while current.left is not None:
        current = current.left
    return current


def is_binary_search_tree(root: Node) -> bool:
    """
    Returns whether the tree is a valid binary search tree. Hint:
    Recursive function. You can under some assumptions make use of
    get_smallest_greater_value and get_greatest_smaller_value --> this threw me off so hard.

    :param root: The root of the (sub)tree
    :return: true iff it is a valid binary search tree
    """
    if root is None:
        return True
    
    if root.left is not None:
        if root.left.info > root.info:
            return False
    if root.right is not None:
        if root.info > root.right.info:
            return False

    return is_binary_search_tree(root.left) and is_binary_search_tree(root.right)



def search(root: Node, value: int) -> typing.Tuple[Node, typing.Optional[Node]]:
    """
    Given a binary search tree, returns a Tuple with the following two items:
     - the parent of the node with a certain value
     - the node with a certain value
    Note that having access to the parent will prove useful
    other functions, such as adding and removing.

    If the tree does not contain the value, return
    the parent of the node where it should have been
    placed, and a None value.

    :param root: The root of the (sub)tree
    :return: tuple of the nodes as described above
    """

    parent = None
    current = root

    while current is not None:
        if current.info == value:
            return (parent, current)
        
        parent = current

        if current.info > value:
            current = current.left
        else:
            current = current.right

    return (parent, None)
    
    
    


def add(root: Node, value: int) -> bool:
    """
    Adds a new node to the binary search tree, respecting the condition that
    for each node all values in the left sub-tree are smaller than its value,
    and all values in the right subtree are greater than its value.
    Only adds the node with the value, if it does not exist yet in the tree.

    You should also mention that this node is added as a leaf and not in the middle of the tree.

    :param root: the root of the (sub)tree
    :param value: the value to be added
    :return: true upon success, false upon failure
    """
    parent, node = search(root, value)

    if node is not None:
        return False
    
    new_node = Node(value, None, None)

    if value < parent.info:
        parent.left = new_node
    else:
        parent.right = new_node

    return True


def remove(root: Node, value: int) -> bool:
    """
    Removes a node from the binary search tree, respecting the condition that
    for each node all values in the left sub-tree are smaller than its value,
    and all values in the right subtree are greater than its value.
    Only removes the node with the value, if it does exist in the tree.
    Hint: use get_greatest_smaller or get_smalnlest_greater values.

    :param root: the root of the (sub)tree
    :param value: the value to be deleted
    :return: true upon success, false upon failure
    """
    parent, node = search(root, value)

    if node is None:
        return False

    # if node is a leaf, we make its parent's child (node) none
    if node.left is None and node.right is None:
        if parent is None:
            root = None
        elif parent.left == node:
            parent.left = None
        else:
            parent.right = None

    # if node has only one child, remove node and place its child right or left depending on where the node was
    elif node.left is None:  
        if parent is None:
            root = node.right
        elif parent.left == node:
            parent.left = node.right
        else:
            parent.right = node.right

    elif node.right is None:
        if parent is None:
            root = node.left
        elif parent.left == node:
            parent.left = node.left
        else:
            parent.right = node.left

    # if node has two children, we use smallest greater value instead of it, then remove the previous sgv as a leaf
    else:
        sgv = get_smallest_greater_value(node)
        sgv_value = sgv.info
        remove(root, sgv_value)
        node.info = sgv_value
    
    # we may have used gsv as well

    return True

