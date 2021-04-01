class AVLNode(object):
    def __init__(self, key, left_child=None, right_child=None):
        # key/data/value of the node
        self.data = key
        # Children of this node
        self.left = left_child
        self.right = right_child

    def __str__(self, node=None):
        if node is None:
            return '\n'.join(self.__str__(self))
        strings = []
        if node.right is not None:
            for right_string in self.__str__(node.right):
                strings.append(5 * ' ' + right_string.replace('->', '/-', 1))
        c = 98 - 7 * node.colour
        strings.append('-> \033['+str(c)+'m ({})\033[00m'.format(repr(node.data)))
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


class AVL(object):
    def __init__(self):
        self.root = None

    def __str__(self, TN=None):
        if TN is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def height(self, TN: AVLNode):
        h = 0
        if TN is not None:
            l_height = self.height(TN.left)
            r_height = self.height(TN.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

    def getBalance(self, TN: AVLNode):
        if not TN:
            return 0

        return self.height(TN.left) - self.height(TN.right)

    def _insert(self, TN, data):
        # Standard BST insertion
        if TN is None:
            return AVLNode(data)

        if data < TN.data:
            TN.left = self._insert(TN.left, data)
        else:
            TN.right = self._insert(TN.right, data)

        # Balancing
        balance = self.getBalance(TN)

        if balance > 1 and data < TN.left.data:
            return self.rightRotate(TN)

        if balance < -1 and data > TN.right.data:
            return self.leftRotate(TN)

        if balance > 1 and data > TN.left.data:
            TN.left = self.leftRotate(TN.left)
            return self.rightRotate(TN)

        if balance < -1 and data < TN.right.data:
            TN.right = self.rightRotate(TN.right)
            return self.leftRotate(TN)

        return TN

    def insert(self, data):
        if self.root is None:
            self.root = AVLNode(data)
        else:
            self.root = self._insert(self.root, data)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def _delete(self, TN, data):

        # Perform standard BST delete
        if not TN:
            return TN

        elif data < TN.data:
            TN.left = self._delete(TN.left, data)

        elif data > TN.data:
            TN.right = self._delete(TN.right, data)

        else:
            if TN.left is None:
                temp = TN.right
                TN = None
                return temp

            elif TN.right is None:
                temp = TN.left
                TN = None
                return temp

            temp = self.getMinValueNode(TN.right)
            TN.data = temp.data
            TN.right = self._delete(TN.right, temp.data)

        if TN is None:
            return TN

        # Balancing
        balance = self.getBalance(TN)

        if balance > 1 and self.getBalance(TN.left) >= 0:
            return self.rightRotate(TN)

        if balance < -1 and self.getBalance(TN.right) <= 0:
            return self.leftRotate(TN)

        if balance > 1 and self.getBalance(TN.left) < 0:
            TN.left = self.leftRotate(TN.left)
            return self.rightRotate(TN)

        if balance < -1 and self.getBalance(TN.right) > 0:
            TN.right = self.rightRotate(TN.right)
            return self.leftRotate(TN)

        return TN

    def delete(self, *args):
        if type(args[0]) == list:  # otherwise it is given as a tuple
            args = args[0]
        for data in args:
            self.root = self._delete(self.root, data)

    @staticmethod
    def leftRotate(TN):
        TN1 = TN.right
        TN2 = TN1.left
        TN1.left = TN
        TN.right = TN2
        return TN1

    @staticmethod
    def rightRotate(TN):
        TN1 = TN.left
        TN2 = TN1.right
        TN1.right = TN
        TN.left = TN2
        return TN1


def __test__():
    avl = AVL()
    # First insert into None node (create root)
    avl.insert(10)
    avl.insert(20)
    avl.insert(30)
    avl.insert(40)
    avl.insert(25)
    #
    avl.insert(50)
    print(avl)
    print("*****************************")
    avl.delete(40, 50)
    print(avl)
    print("*****************************")
    # AVL.delete(50)
    # # AVL.root = AVL.balance(AVL.root)

    print(avl)
    # print(AVL)
    # AVL.insert(40)
    # print("*****************************")
    # print(AVL)


__test__()
