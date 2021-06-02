RED = 1
BLACK = 0


def isRed(h):
    return isinstance(h, Node) and h.colour == RED


def isBlack(h):
    return not isRed(h)


class Node:
    """
    Node class for an RB Tree

    Node is a basic node object with a key,  2 children, height and colour.

    A string function is provided for nice printing of the tree.

    Infix is provided with a number of other RB related functions.
    """
    def __init__(self, key=None, left_child=None, right_child=None, colour=RED):
        self.key = key
        self.left = left_child
        self.right = right_child
        # Colour of node 1 is red/ 0 is black
        self.colour = colour
        self.height = 0

    def __str__(self, node=None, notebook=True):
        """
        Pretty prints the tree. Text colour represents the node colour
        :param node: current node in traversal
        :return: node in a pretty string format
        """
        if node is None:
            return '\n'.join(self.__str__(self))
        strings = []
        if node.right is not None:
            for right_string in self.__str__(node.right):
                strings.append(5 * ' ' + right_string.replace('->', '/-', 1))
        c = 98 - 7 * node.colour
        if not notebook:
            strings.append('-> \033[' + str(c) + 'm ({})\033[00m'.format(repr(node.key)))
        else:
            strings.append('-> ({})'.format(repr(node.key)))
        if node.left is not None:
            for left_string in self.__str__(node.left):
                strings.append(5 * ' ' + left_string.replace('->', '\\-', 1))
        return strings

    def traverseInfix(self, result=None):
        """
        Infix traversal of the tree
        :param result: tree in infix so far
        :return: a list of nodes of the tree, in infix
        """
        if result is None:
            result = []

        if self.left:
            self.left.traverseInfix(result)

        result.append(self.key)

        if self.right:
            self.right.traverseInfix(result)

        return result

    def min(self, tree):
        """
        :param tree: tree node makes part of
        :return: key if it this node is smallest in the tree
        """
        tree.comparisons += 1
        return self.key if self.left is None else self.left.min(tree)

    def max(self, tree):
        """
        :param tree: tree node makes part of
        :return: key if it this node is largest in the tree
        """
        tree.comparisons += 1
        return self.key if self.right is None else self.right.max(tree)

    def fixUp(self, tree):
        """
        Fixes tree on the way up after deletion
        :param tree: tree that needs fixing
        :return: fixed tree
        """
        tree.comparisons += 1
        if isRed(self.right):
            tree.rotations += 1
            self = self.rotateLeft()

        tree.comparisons += 3
        # Double red on left case
        if isRed(self.left) and self.left and isRed(self.left.left):
            tree.rotations += 1
            self = self.rotateRight()

        tree.comparisons += 2
        # Both children are red
        if isRed(self.left) and isRed(self.right):
            self.flipColours(tree)

        return self

    def flipColours(self, tree):
        """
        Flips the colours of a tree's immediate children
        :param tree: Tree that will have its children's colours flipped
        :return: Tree with children's colour flipped
        """
        tree.comparisons += 1
        self.colour = 0 if self.colour == 1 else 1

        tree.comparisons += 1
        if self.left is not None:
            tree.comparisons += 1
            self.left.colour = 0 if self.left.colour == 1 else 1

        tree.comparisons += 1
        if self.right is not None:
            tree.comparisons += 1
            self.right.colour = 0 if self.right.colour == 1 else 1

    def rotateLeft(self):
        """
        Rotates current node to the left
        :return: Rotated subtree
        """
        x = self.right
        self.right = x.left
        x.left = self
        x.colour = self.colour
        self.colour = 1
        return x

    def rotateRight(self):
        """
        Rotates current node to the right
        :return: Rotated subtree
        """
        x = self.left
        self.left = x.right
        x.right = self
        x.colour = self.colour
        self.colour = 1
        return x

    def moveRedLeft(self, tree):
        """
        Does a Left Right rotation and fixes colours
        :param tree: Tree that needs rotation
        :return: Rotated subtree
        """
        self.flipColours(tree)
        tree.comparisons += 2
        if self.right and isRed(self.right.left):
            tree.rotations += 2
            self.right = self.right.rotateRight()
            self = self.rotateLeft()
            self.flipColours(tree)
        return self

    def moveRedRight(self, tree):
        """
        Does a Right rotation and fixes colours
        :param tree: Tree that needs rotation
        :return: Rotated subtree
        """
        self.flipColours(tree)
        tree.comparisons += 2
        if self.left and isRed(self.left.left):
            tree.rotations += 1
            self = self.rotateRight()
            self.flipColours(tree)
        return self

    def deleteMin(self, tree):
        """
        Deletes smallest node in tree
        :param tree:
        :return: Removes smallest node from tree
        """
        tree.comparisons += 1
        if self.left is None:
            return None

        tree.comparisons += 3
        if isBlack(self.left) and self.left and isBlack(self.left.left):
            self = self.moveRedLeft(tree)

        self.left = self.left.deleteMin(tree)

        return self.fixUp(tree)

    def deleteMax(self, tree):
        """
        Deletes largest node in tree
        :param tree:
        :return: Removes largest node from tree
        """
        tree.comparisons += 1
        if isRed(self.left):
            tree.rotations += 1
            self = self.rotateRight()

        tree.comparisons += 1
        if self.right is None:
            return None

        tree.comparisons += 3
        if isBlack(self.right) and self.right and isBlack(self.right.left):
            self = self.moveRedRight(tree)

        self.right = self.right.deleteMax(tree)

        return self.fixUp(tree)



class LLRBT:
    """
    Left Leaning Red Black tree class which contains operations that make up and define an LLRB tree.

    rotation and comparison counts are kept for tree comparison
    """
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.comparisons = 0

    def __str__(self, RBTN=None, notebook=True):
        """
        Starts pretty print process
        :param RBTN: Node from which
        :return: pretty print of the tree
        """
        if RBTN is None:
            if self.root is None:
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root, notebook))

    def isEmpty(self):
        """
        :return: Whether tree is empty or not
        """
        return self.root is None

    def search(self, key):
        """
        :param key: Key of node
        :return: Returns Node if found, None if not found
        """
        x = self.root
        self.comparisons += 1
        while x is not None:
            self.comparisons += 3
            if key == x.key:
                self.comparisons -= 2
                return x.key
            elif key < x.key:
                self.comparisons -= 1
                x = x.left
            elif key > x.key:
                x = x.right
            self.comparisons += 1
        return None

    def insert(self, key):
        """
        Inserts key in tree using the recursive _insert function
        """
        self.root = self._insert(self.root, key)
        self.root.colour = 0

    def _insert(self, h: Node, key):
        """
        Recursive helper function to insert key into the tree
        :param h: Current sub tree root node
        :param key: key to be inserted
        :return: height updated tree with key inserted
        """
        if h is None:
            return Node(key)

        self.comparisons += 2
        if isRed(h.left) and isRed(h.right):
            h.flipColours(self)

        self.comparisons += 3
        if key == h.key:
            self.comparisons -= 2
        elif key < h.key:
            self.comparisons -= 1
            h.left = self._insert(h.left, key)
        else:
            h.right = self._insert(h.right, key)

        self.comparisons += 2
        if isBlack(h.left) and isRed(h.right):
            self.rotations += 1
            h = h.rotateLeft()

        self.comparisons += 2
        if isRed(h.left) and isRed(h.left.left):
            self.rotations += 1
            h = h.rotateRight()

        return h

    def delete(self, key):
        """
        Deletes key from tree
        """
        res = self.search(key)

        self.comparisons += 1
        if res is None:
            return False

        self.comparisons += 2
        if isBlack(self.root.left) and isBlack(self.root.right):
            self.root.color = RED

        self.comparisons += 1
        if self.root is not None:
            self.root = self._delete(self.root, key)

        self.comparisons += 1
        if not self.isEmpty():
            self.root.color = BLACK

    def _delete(self, h: Node, key):
        """
        Recursive helper function to delete key from the tree
        :param h: Current sub tree root node
        :param key: key to be removed
        :return: tree with key removed
        """

        self.comparisons += 1
        if key < h.key:
            self.comparisons += 2
            if isBlack(h.left) and h.left and isBlack(h.left.left):
                h = h.moveRedLeft(self)
            h.left = self._delete(h.left, key)
        else:

            self.comparisons += 1
            if isRed(h.left):
                h = h.rotateRight()

            self.comparisons += 2
            if key == h.key and h.right is None:
                return None

            self.comparisons += 3
            if isBlack(h.right) and h.right and isBlack(h.right.left):
                h = h.moveRedRight(self)

            self.comparisons += 1
            if key == h.key:
                h.key = h.right.min(self)
                h.right = h.right.deleteMin(self)
            else:
                h.right = self._delete(h.right, key)

        return h.fixUp(self)

    def deleteMin(self):
        """
        Remove smallest Node from tree
        """
        self.root = self.root.deleteMin(self)
        self.root.color = BLACK

    def deleteMax(self):
        """
        Remove largest Node from tree
        """
        self.root = self.root.deleteMax(self)
        self.root.color = BLACK

    def min(self):
        """
        :return: None if root is None, else the smallest node
        """
        self.comparisons += 1
        return None if self.root is None else self.root.min(self)

    def max(self):
        """
        :return: None if root is None, else the largest node
        """
        self.comparisons += 1
        return None if self.root is None else self.root.max(self)

    def height(self, RBNode: Node):
        """
        Gets height of RBNode i.e. distance from it to the deepest node in its sub tree.
        :param Node: Starting Node
        :return: height
        """
        h = 0
        self.comparisons += 1
        if RBNode is not None:
            l_height = self.height(RBNode.left)
            r_height = self.height(RBNode.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

rbt = LLRBT()
rbt.insert(10)
rbt.insert(15)
rbt.insert(20)
rbt.insert(25)
rbt.insert(30)
rbt.insert(35)
rbt.insert(40)
rbt.insert(45)

print(rbt)
print(rbt.height(rbt.root))
