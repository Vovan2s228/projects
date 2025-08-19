import numpy as np
RNG = np.random.default_rng()

class Node():
    def __init__(self, value, left=None, middle=None, right=None):
        """
        This is a node for a ternary tree.

        Attributes:
            :param info: The value of the node.
            :type: info: int
            :param left: The left child of the node, defaults to None
            :type left: Node, optional
            :param middle: The middle child of the node, defaults to None
            :type middle: Node, optional
            :param right: The right child of the node, defaults to None
            :type right: Node, optional
        """
        self.info = value
        self.left = left
        self.middle = middle
        self.right = right

    def __repr__(self):
        return f"Node({self.info}) -> {self.left.info if self.left is not None else 'None', self.middle.info if self.middle is not None else 'None', self.right.info if self.right is not None else 'None'}"

class TernaryTree():
    def __init__(self):
        """
        This initializes the tree which is always initialized as an empty tree.

        Attributes:
            :param root: The root of the tree
            :type root: Node
        """
        self.root = None

    def add(self, value):
        """
        Randomly add values to the tree.
        You could do this by randomly traversing the tree and
        add a new node when a empty leaf node is found.

        :param value: The value that is added to the tree
        :type value: int
        """
        # raise NotImplementedError("Please complete this method")
        if self.root is None:
            self.root = Node(value)
            return

        current = self.root
        while True:
            choice = RNG.choice([0, 1, 2])
            if choice == 0 and current.left is None:
                current.left = Node(value)
                return
            elif choice == 1 and current.middle is None:
                current.middle = Node(value)
                return
            elif choice == 2 and current.right is None:
                current.right = Node(value)
                return

            current = [current.left, current.middle, current.right][choice]
