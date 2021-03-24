# Adapted from book
import Node


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


# class RBTNil(object):
#     def __init__(self, root):
#         self.root = root
#         self.colour = 0

# noinspection DuplicatedCode
class RBT(object):
    def __init__(self, root=None):
        self.root = root

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

        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent

        if y.left is None:
            self.root = y
        elif x is x.parent.left:
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

        if y.right is not None:
            y.right.parent = x

        y.parent = x.parent

        if y.right is None:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    def _insertFix(self, z):
        if z.parent is not None:
            if z.parent.parent is not None:
                while z.parent.colour == 1:
                    if z.parent is z.parent.parent.left:
                        y = z.parent.parent.right
                        if y is not None:
                            if y.colour == 1:
                                z.parent.colour = 0
                                y.colour = 0
                                z.parent.parent.colour = 1
                                z = z.parent.parent
                            elif z is z.parent.right:
                                z = z.parent
                                self.LeftRotate(z)
                            else:
                                z.parent.colour = 0
                                z.parent.parent.colour = 1
                                self.RightRotate(z.parent.parent)
                    else:
                        y = z.parent.parent.left
                        if y is not None:
                            if y.colour == 1:
                                z.parent.colour = 0
                                y.colour = 0
                                z.parent.parent.colour = 1
                                z = z.parent.parent
                            elif z is z.parent.left:
                                z = z.parent
                                self.RightRotate(z)
                            else:
                                z.parent.colour = 0
                                z.parent.parent.colour = 1
                                self.LeftRotate(z.parent.parent)
        self.root.colour = 0

    def insert(self, z):
        z = RBTNode(key=z)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = None
        z.right = None
        z.colour = 1
        self._insertFix(z)


rbt = RBT()
# rbt.Insert(10)
# rbt.Insert(15)
# rbt.Insert(5)

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
