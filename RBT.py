class RBTNode(object):
    """
    Node class for an RB Tree

    Based on a basic node object with the addition of the colour of the node as well as a reference of the parent.
    A reference is kept to make fixing the double red mistake easier to fix.

    A string function is provided for clean printing of the tree. - Credit guy

    Infix, postfix and prefix is traversing is also provided.
    """
    def __init__(self, key=None, left_child=None, right_child=None, parent=None, colour=0):
        self.key = key
        self.left = left_child
        self.right = right_child
        # If parent is none then it is root of entire tree
        self.parent = parent
        # Colour of node 1 is red/ 0 is black
        self.colour = colour

    def __str__(self, node=None):
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

    def traverse_infix(self, result=None):
        if result is None:
            result = []

        if self.left:
            self.left.traverse_infix(result)

        result.append(self.key)

        if self.right:
            self.right.traverse_infix(result)

        return result

    def traverse_prefix(self, result=None):
        if result is None:
            result = []

        result.append(self.key)

        if self.left:
            self.left.traverse_prefix(result)

        if self.right:
            self.right.traverse_prefix(result)

        return result

    def traverse_postfix(self, result=None):
        if result is None:
            result = []

        if self.left:
            self.left.traverse_postfix(result)

        if self.right:
            self.right.traverse_postfix(result)

        result.append(self.key)

        return result


class RBT(object):
    """
    RB tree class which contains operations that make up and define an RB tree.

    A Null node is kept as TNULL as I found it easier to implement the tree with it as well as it makes for better
    visualization.

    rotation, node and comparison counts are kept for tree comparison
    """
    def __init__(self):
        self.TNULL = RBTNode(0)
        self.TNULL.colour = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.rotations = 0
        self.nodes = 0
        self.comparisons = 0

    def __str__(self, TN=None):
        if TN is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def LeftRotate(self, x):
        self.comparisons += 1
        if x is None:
            raise Exception("x cannot be None")
        y = x.right
        x.right = y.left
        self.comparisons += 1
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        self.comparisons += 2
        if x.parent is None:
            self.comparisons -= 1
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.rotations += 1

    def RightRotate(self, x):
        self.comparisons += 1
        if x is None:
            raise Exception("x cannot be None")
        y = x.left
        x.left = y.right
        self.comparisons += 1
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        self.comparisons += 2
        if x.parent is None:
            self.comparisons -= 1
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self.rotations += 1

    def _insertFix(self, key):
        self.comparisons += 1
        while key.parent.colour == 1:
            self.comparisons += 1
            if key.parent == key.parent.parent.right:
                u = key.parent.parent.left  # uncle
                self.comparisons += 1
                if u.colour == 1:
                    u.colour = 0
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    key = key.parent.parent
                else:
                    self.comparisons += 1
                    if key == key.parent.left:
                        key = key.parent
                        self.RightRotate(key)
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    self.LeftRotate(key.parent.parent)
            else:
                u = key.parent.parent.right  # uncle

                self.comparisons += 1
                if u.colour == 1:
                    # mirror case 3.1
                    u.colour = 0
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    key = key.parent.parent
                else:
                    self.comparisons += 1
                    if key == key.parent.right:
                        # mirror case 3.2.2
                        key = key.parent
                        self.LeftRotate(key)
                    # mirror case 3.2.1
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    self.RightRotate(key.parent.parent)
            self.comparisons += 1
            if key == self.root:
                break

            self.comparisons += 1
        self.root.colour = 0

    def insert(self, key):
        self.nodes += 1
        # Ordinary Binary Search Insertion
        node = RBTNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.colour = 1  # new node must be red

        y = None
        x = self.root

        self.comparisons += 1
        while x != self.TNULL:
            y = x

            self.comparisons += 1
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

            self.comparisons += 1

        # y is parent of x
        node.parent = y

        self.comparisons += 2
        if y is None:

            self.comparisons -= 1
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        # if new node is a root node, simply return
        self.comparisons += 1
        if node.parent is None:
            node.colour = 0
            return

        # if the grandparent is None, simply return
        self.comparisons += 1
        if node.parent.parent is None:
            return

        # Fix the tree
        self._insertFix(node)

    def __fix_delete(self, x):

        self.comparisons += 1
        while x != self.root and x.colour == 0:

            self.comparisons += 1
            if x == x.parent.left:
                s = x.parent.right

                self.comparisons += 1
                if s.colour == 1:
                    # case 3.1
                    s.colour = 0
                    x.parent.colour = 1
                    self.LeftRotate(x.parent)
                    s = x.parent.right

                self.comparisons += 2
                if s.left.colour == 0 and s.right.colour == 0:
                    # case 3.2
                    s.colour = 1
                    x = x.parent
                else:

                    self.comparisons += 1
                    if s.right.colour == 0:
                        # case 3.3
                        s.left.colour = 0
                        s.colour = 1
                        self.RightRotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.colour = x.parent.colour
                    x.parent.colour = 0
                    s.right.colour = 0
                    self.LeftRotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left

                self.comparisons += 1
                if s.colour == 1:
                    # case 3.1
                    s.colour = 0
                    x.parent.colour = 1
                    self.RightRotate(x.parent)
                    s = x.parent.left

                self.comparisons += 2
                if s.left.colour == 0 and s.right.colour == 0:
                    # case 3.2
                    s.colour = 1
                    x = x.parent
                else:

                    self.comparisons += 1
                    if s.left.colour == 0:
                        # case 3.3
                        s.right.colour = 0
                        s.colour = 1
                        self.LeftRotate(s)
                        s = x.parent.left

                    # case 3.4
                    s.colour = x.parent.colour
                    x.parent.colour = 0
                    s.left.colour = 0
                    self.RightRotate(x.parent)
                    x = self.root

            self.comparisons += 1
        x.colour = 0

    def _delete(self, node, key):
        # find the node containing key
        z = self.TNULL
        self.comparisons += 1
        while node != self.TNULL:

            self.comparisons += 1
            if node.key == key:
                z = node

            self.comparisons += 1
            if node.key <= key:
                node = node.right
            else:
                node = node.left

            self.comparisons += 1

        self.comparisons += 1
        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_colour = y.colour

        self.comparisons += 2
        if z.left == self.TNULL:

            self.comparisons -= 1
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_colour = y.colour
            x = y.right

            self.comparisons += 1
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.colour = z.colour

        self.comparisons += 1
        if y_original_colour == 0:
            self.__fix_delete(x)

    def minimum(self, node):
        self.comparisons += 1
        while node.left != self.TNULL:
            node = node.left
            self.comparisons += 1
        return node

    def maximum(self, node):
        self.comparisons += 1
        while node.right != self.TNULL:
            node = node.right
            self.comparisons += 1
        return node

    def __rb_transplant(self, u, v):

        self.comparisons += 2
        if u.parent is None:
            self.comparisons -= 1
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, *args):
        self.comparisons += 1
        if type(args[0]) == list:  # otherwise it is given as a tuple
            args = args[0]

        self.comparisons += 1
        for key in args:
            self.nodes -= 1
            self._delete(self.root, key)
            self.comparisons += 1
