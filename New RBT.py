# Adapted from book


class RBTNode(object):
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


class RBT(object):
    def __init__(self, root=None):
        self.TNULL = RBTNode(0)
        self.TNULL.colour = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def __str__(self, TN=None):
        if TN is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def LeftRotate(self, x):
        if x is None:
            raise Exception("x cannot be None")
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RightRotate(self, x):
        if x is None:
            raise Exception("x cannot be None")
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _insertFix(self, key):
        while key.parent.colour == 1:
            if key.parent == key.parent.parent.right:
                u = key.parent.parent.left  # uncle
                if u.colour == 1:
                    u.colour = 0
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    key = key.parent.parent
                else:
                    if key == key.parent.left:
                        key = key.parent
                        self.RightRotate(key)
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    self.LeftRotate(key.parent.parent)
            else:
                u = key.parent.parent.right  # uncle

                if u.colour == 1:
                    # mirror case 3.1
                    u.colour = 0
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    key = key.parent.parent
                else:
                    if key == key.parent.right:
                        # mirror case 3.2.2
                        key = key.parent
                        self.LeftRotate(key)
                    # mirror case 3.2.1
                    key.parent.colour = 0
                    key.parent.parent.colour = 1
                    self.RightRotate(key.parent.parent)
            if key == self.root:
                break
        self.root.colour = 0

    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = RBTNode(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.colour = 1  # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y is None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        # if new node is a root node, simply return
        if node.parent is None:
            node.color = 0
            return

        # if the grandparent is None, simply return
        if node.parent.parent is None:
            return

        # Fix the tree
        self._insertFix(node)

    def __fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.LeftRotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        # case 3.3
                        s.left.color = 0
                        s.color = 1
                        self.RightRotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.LeftRotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.RightRotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.color = 1
                        self.LeftRotate(s)
                        s = x.parent.left

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.RightRotate(x.parent)
                    x = self.root
        x.color = 0

    def _delete(self, node, key):
        # find the node containing key
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def __rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, *args):
        if type(args[0]) == list:  # otherwise it is given as a tuple
            args = args[0]
        for data in args:
            self.root = self._delete(self.root, data)


rbt = RBT()

rbt.insert(5)
rbt.insert(10)
rbt.insert(15)
rbt.insert(20)
rbt.insert(30)
rbt.insert(40)
rbt.insert(50)
rbt.insert(55)
rbt.insert(60)
rbt.insert(65)
rbt.insert(70)
rbt.insert(80)
rbt.insert(85)
rbt.insert(90)
rbt.insert(45)

print(rbt)