RED = 1
BLACK = 0


def is_red(h):
    return isinstance(h, Node) and h.colour == RED


def is_black(h):
    return not is_red(h)


class Node:
    def __init__(self, key=None, left_child=None, right_child=None, colour=RED):
        self.key = key
        self.left = left_child
        self.right = right_child
        # Colour of node 1 is red/ 0 is black
        self.colour = colour
        self.height = 0

    def __str__(self, node=None):
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
        strings.append('-> \033[' + str(c) + 'm ({})\033[00m'.format(repr(node.key)))
        if node.left is not None:
            for left_string in self.__str__(node.left):
                strings.append(5 * ' ' + left_string.replace('->', '\\-', 1))
        return strings

    def min(self, tree):
        tree.comparisons += 1
        return self.key if self.left is None else self.left.min(tree)

    def max(self, tree):
        tree.comparisons += 1
        return self.key if self.right is None else self.right.max(tree)

    def fix_up(self, tree):
        tree.comparisons += 1
        if is_red(self.right):
            tree.rotations += 1
            self = self.rotateLeft()

        tree.comparisons += 2
        if is_red(self.left) and self.left and is_red(self.left.left):
            tree.rotations += 1
            self = self.rotateRight()

        tree.comparisons += 2
        if is_red(self.left) and is_red(self.right):
            self.flipColours(tree)

        return self.setHeight()

    def flipColours(self, tree):
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
        x = self.right
        self.right = x.left
        x.left = self
        x.colour = self.colour
        self.colour = 1
        return x

    def rotateRight(self):
        x = self.left
        self.left = x.right
        x.right = self
        x.colour = self.colour
        self.colour = 1
        return x

    def move_red_left(self, tree):
        self.flipColours(tree)
        tree.comparisons += 2
        if self.right and is_red(self.right.left):
            tree.rotations += 2
            self.right = self.right.rotateRight()
            self = self.rotateLeft()
            self.flipColours(tree)
        return self

    def move_red_right(self, tree):
        self.flipColours(tree)
        tree.comparisons += 2
        if self.left and is_red(self.left.left):
            tree.rotations += 1
            self = self.rotateRight()
            self.flipColours(tree)
        return self

    def delete_min(self, tree):
        tree.comparisons += 1
        if self.left is None:
            return None

        tree.comparisons += 3
        if is_black(self.left) and self.left and is_black(self.left.left):
            self = self.move_red_left(tree)

        self.left = self.left.delete_min(tree)

        return self.fix_up(tree)

    def delete_max(self, tree):
        tree.comparisons += 1
        if is_red(self.left):
            tree.rotations += 1
            self = self.rotateRight()

        tree.comparisons += 1
        if self.right is None:
            return None

        tree.comparisons += 3
        if is_black(self.right) and self.right and is_black(self.right.left):
            self = self.move_red_right(tree)

        self.right = self.right.delete_max(tree)

        return self.fix_up(tree)

    def setHeight(self):
        self.height = 1 + max(self.left and self.left.height or 0,
                              self.right and self.right.height or 0)
        return self


class LLRBT:
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.nodes = 0
        self.comparisons = 0

    def __str__(self, RBTN=None):
        """
        Starts pretty print process
        :param RBTN: Node from which
        :return: pretty print of the tree
        """
        if RBTN is None:
            if self.root is None:
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        self.comparisons += 1
        return self.root is None

    def search(self, key):
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
        self.root = self._insert(self.root, key)
        self.root.colour = 0

    def _insert(self, h: Node, key):
        if h is None:
            self.nodes += 1
            return Node(key)

        self.comparisons += 2
        if is_red(h.left) and is_red(h.right):
            h.flipColours(self)

        self.comparisons += 3
        if key == h.key:
            self.comparisons -= 2
            #print("Key already inserted")
        elif key < h.key:
            self.comparisons -= 1
            h.left = self._insert(h.left, key)
        else:
            h.right = self._insert(h.right, key)

        self.comparisons += 2
        if is_black(h.left) and is_red(h.right):
            self.rotations += 1
            h = h.rotateLeft()

        self.comparisons += 2
        if is_red(h.left) and is_red(h.left.left):
            self.rotations += 1
            h = h.rotateRight()

        return h.setHeight()

    def delete(self, key):
        res = self.search(key)

        self.comparisons += 1
        if res is None:
            #print("Tree does not contain key '{0}'.\n".format(key))
            return False

        self.comparisons += 2
        if is_black(self.root.left) and is_black(self.root.right):
            self.root.color = RED

        self.comparisons += 1
        if self.root is not None:
            self.nodes -= 1
            self.root = self._delete(self.root, key)

        self.comparisons += 1
        if not self.is_empty():
            self.root.color = BLACK

    def _delete(self, h, key):
        """
        Delete a node with the given key (recursively) from the tree below.
        """
        assert self.search(key) is not None

        self.comparisons += 1
        if key < h.key:
            self.comparisons += 2
            if is_black(h.left) and h.left and is_black(h.left.left):
                h = h.move_red_left(self)
            h.left = self._delete(h.left, key)
        else:

            self.comparisons += 1
            if is_red(h.left):
                h = h.rotateRight()

            self.comparisons += 2
            if key == h.key and h.right is None:
                return None

            self.comparisons += 3
            if is_black(h.right) and h.right and is_black(h.right.left):
                h = h.move_red_right(self)

            self.comparisons += 1
            if key == h.key:
                h.key = h.right.min(self)
                h.right = h.right.delete_min(self)
            else:
                h.right = self._delete(h.right, key)

        return h.fix_up(self)

    def delete_min(self):
        self.root = self.root.delete_min(self)
        self.root.color = BLACK

    def delete_max(self):
        self.root = self.root.delete_max(self)
        self.root.color = BLACK

    def min(self):
        self.comparisons += 1
        return None if self.root is None else self.root.min(self)

    def max(self):
        self.comparisons += 1
        return None if self.root is None else self.root.max(self)


rbt = LLRBT()
rbt.insert(10)
rbt.insert(15)
rbt.insert(20)
rbt.insert(25)
rbt.insert(30)
rbt.insert(35)
rbt.insert(40)
rbt.insert(45)
rbt.delete(40)
rbt.delete(20)
print(rbt)
