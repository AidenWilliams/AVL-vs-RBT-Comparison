class AVLNode(object):
    """
    Node class for an AVL Tree

    AVLNode is a basic node object with a key and 2 children.

    A string function is provided for clean printing of the tree. - Credit guy

    Infix, postfix and prefix is traversing is also provided.
    """
    def __init__(self, key, left_child=None, right_child=None):
        # key/data/value of the node
        self.key = key
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
        strings.append('-> \033[98m ({})\033[00m'.format(repr(node.key)))
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
    """
    AVL tree class which contains operations that make up and define an AVL tree.

    rotation, node and comparison counts are kept for tree comparison
    """
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.nodes = 0
        self.comparisons = 0

    def __str__(self, AVLN=None):
        if AVLN is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def height(self, AVLN: AVLNode):
        h = 0
        self.comparisons += 1
        if AVLN is not None:
            l_height = self.height(AVLN.left)
            r_height = self.height(AVLN.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

    def getBalance(self, AVLN: AVLNode):
        if not AVLN:
            return 0

        return self.height(AVLN.left) - self.height(AVLN.right)

    def _insert(self, AVLN, key):
        # Standard BST insertion
        self.comparisons += 1
        if AVLN is None:
            self.nodes += 1
            return AVLNode(key)

        self.comparisons += 1
        if key < AVLN.key:
            AVLN.left = self._insert(AVLN.left, key)
        else:
            AVLN.right = self._insert(AVLN.right, key)

        # Balancing
        balance = self.getBalance(AVLN)

        self.comparisons += 2
        if balance > 1 and key < AVLN.left.key:
            return self.rightRotate(AVLN)

        self.comparisons += 2
        if balance < -1 and key > AVLN.right.key:
            return self.leftRotate(AVLN)

        self.comparisons += 2
        if balance > 1 and key > AVLN.left.key:
            AVLN.left = self.leftRotate(AVLN.left)
            return self.rightRotate(AVLN)

        self.comparisons += 2
        if balance < -1 and key < AVLN.right.key:
            AVLN.right = self.rightRotate(AVLN.right)
            return self.leftRotate(AVLN)

        return AVLN

    def insert(self, key):
        self.comparisons += 1
        if self.root is None:
            self.root = AVLNode(key)
        else:
            self.root = self._insert(self.root, key)

    def getMinValueNode(self, root):
        self.comparisons += 1
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def _delete(self, AVLN, key):

        # Perform standard BST delete
        self.comparisons += 3
        if not AVLN:
            self.comparisons -= 2
            return AVLN

        elif key < AVLN.key:
            self.comparisons -= 1
            AVLN.left = self._delete(AVLN.left, key)

        elif key > AVLN.key:
            AVLN.right = self._delete(AVLN.right, key)

        else:
            self.comparisons += 2
            if AVLN.left is None:
                temp = AVLN.right
                AVLN = None
                return temp

            elif AVLN.right is None:
                self.comparisons -= 1
                temp = AVLN.left
                AVLN = None
                return temp

            temp = self.getMinValueNode(AVLN.right)
            AVLN.key = temp.key
            AVLN.right = self._delete(AVLN.right, temp.key)

        self.comparisons += 1
        if AVLN is None:
            return AVLN

        # Balancing
        balance = self.getBalance(AVLN)

        self.comparisons += 2
        if balance > 1 and self.getBalance(AVLN.left) >= 0:
            return self.rightRotate(AVLN)

        self.comparisons += 2
        if balance < -1 and self.getBalance(AVLN.right) <= 0:
            return self.leftRotate(AVLN)

        self.comparisons += 2
        if balance > 1 and self.getBalance(AVLN.left) < 0:
            AVLN.left = self.leftRotate(AVLN.left)
            return self.rightRotate(AVLN)

        self.comparisons += 2
        if balance < -1 and self.getBalance(AVLN.right) > 0:
            AVLN.right = self.rightRotate(AVLN.right)
            return self.leftRotate(AVLN)

        return AVLN

    def delete(self, key):
        self.nodes -= 1
        self.root = self._delete(self.root, key)

    def leftRotate(self, AVLN):
        AVLN1 = AVLN.right
        AVLN2 = AVLN1.left
        AVLN1.left = AVLN
        AVLN.right = AVLN2
        self.rotations += 1
        return AVLN1

    def rightRotate(self, AVLN):
        AVLN1 = AVLN.left
        AVLN2 = AVLN1.right
        AVLN1.right = AVLN
        AVLN.left = AVLN2
        self.rotations += 1
        return AVLN1

    def search(self, key, node=None):
        self.comparisons += 1
        if node is None:
            node = self.root

        self.comparisons += 3
        if node.key == key:
            self.comparisons -= 2
            return node
        elif node.key > key:
            self.comparisons -= 1
            return self.search(key, node.right)
        else:
            return self.search(key, node.left)

