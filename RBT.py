class RBTNode(object):
    """
    Node class for an RB Tree

    Based on a basic node object with the addition of the colour of the node as well as a reference of the parent.
    A reference is kept to make fixing the double red mistake easier to fix.

    A string function is provided for nice printing of the tree. - Credit guy

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

    def traverse_infix(self, result=None):
        """
        Infix traversal of the tree
        :param result: tree in infix so far
        :return: a list of nodes of the tree, in infix
        """
        if result is None:
            result = []

        if self.left:
            self.left.traverse_infix(result)

        result.append(self.key)

        if self.right:
            self.right.traverse_infix(result)

        return result

    def traverse_prefix(self, result=None):
        """
        Prefix traversal of the tree
        :param result: tree in prefix so far
        :return: a list of nodes of the tree, in prefix
        """
        if result is None:
            result = []

        result.append(self.key)

        if self.left:
            self.left.traverse_prefix(result)

        if self.right:
            self.right.traverse_prefix(result)

        return result

    def traverse_postfix(self, result=None):
        """
        Postfix traversal of the tree
        :param result: tree in postfix so far
        :return: a list of nodes of the tree, in postfix
        """
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

    def height(self, RBTN: RBTNode):
        """
        Gets height of RBTN i.e. distance from it to the deepest node in its sub tree.
        :param RBTN: Starting Node
        :return: height
        """
        h = 0
        self.comparisons += 1
        if RBTN is not None:
            l_height = self.height(RBTN.left)
            r_height = self.height(RBTN.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

    def LeftRotate(self, x):
        """
        Rotates the tree starting from x to the left

        Rotations are explained further in the report.

        :param x: Pivot point for rotation
        :return: Rotated sub tree
        """
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
        """
        Rotates the tree starting from x to the right.

        Rotations are explained further in the report.

        :param x: Pivot point for rotation
        :return: Rotated sub tree
        """
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

    def _insertFix(self, RBTN: RBTNode):
        """
        Helper function used to fix insertion
        :param RBTN: Node that is being checked for fixing
        :return:
        """
        self.comparisons += 1
        while RBTN.parent.colour == 1:
            self.comparisons += 1
            if RBTN.parent == RBTN.parent.parent.right:
                u = RBTN.parent.parent.left  # uncle
                self.comparisons += 1
                if u.colour == 1:
                    u.colour = 0
                    RBTN.parent.colour = 0
                    RBTN.parent.parent.colour = 1
                    RBTN = RBTN.parent.parent
                else:
                    self.comparisons += 1
                    if RBTN == RBTN.parent.left:
                        RBTN = RBTN.parent
                        self.RightRotate(RBTN)
                    RBTN.parent.colour = 0
                    RBTN.parent.parent.colour = 1
                    self.LeftRotate(RBTN.parent.parent)
            else:
                u = RBTN.parent.parent.right  # uncle

                self.comparisons += 1
                if u.colour == 1:
                    # mirror case 3.1
                    u.colour = 0
                    RBTN.parent.colour = 0
                    RBTN.parent.parent.colour = 1
                    RBTN = RBTN.parent.parent
                else:
                    self.comparisons += 1
                    if RBTN == RBTN.parent.right:
                        # mirror case 3.2.2
                        RBTN = RBTN.parent
                        self.LeftRotate(RBTN)
                    # mirror case 3.2.1
                    RBTN.parent.colour = 0
                    RBTN.parent.parent.colour = 1
                    self.RightRotate(RBTN.parent.parent)
            self.comparisons += 1
            if RBTN == self.root:
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
        # new node must be red
        node.colour = 1

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

    def _delete(self, node, key, verbose=False):
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
            if verbose:
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
            y = self.getMinValueNode(z.right)
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

    def getMinValueNode(self, root: RBTNode):
        """
        Finds the node with smallest key for a sub tree starting in root
        :param root: root of sub tree
        :return: AVLNode with smallest key value
        """
        self.comparisons += 1
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

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

    def delete(self, key):
        self.comparisons += 1
        self.nodes -= 1
        self._delete(self.root, key)

    def search(self, key, RBTN):
        """
        Searches for node with key as its key value
        :param key: key value of the node that needs to be found
        :param RBTN: root of current sub tree
        :return: AVLNode with key as its key
        """
        self.comparisons += 1
        if RBTN is None:
            return None

        self.comparisons += 3
        if RBTN.key == key:
            self.comparisons -= 2
            return RBTN
        elif RBTN.key > key:
            self.comparisons -= 1
            return self.search(key, RBTN.right)
        else:
            return self.search(key, RBTN.left)
