class AVLNode(object):
    """
    Node class for an AVL Tree

    AVLNode is a basic node object with a key and 2 children.

    A string function is provided for nice printing of the tree.

    Infix, postfix and prefix is traversing is also provided.
    """

    def __init__(self, key, left_child=None, right_child=None):
        # key/data/value of the node
        self.key = key
        # Children of this node
        self.left = left_child
        self.right = right_child

    def __str__(self, node=None):
        """
        Pretty prints the tree.
        :param node: current node in traversal
        :return: node in a pretty string format
        """
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
        """
        Starts pretty print process
        :param AVLN: Node from which
        :return: pretty print of the tree
        """
        if AVLN is None:
            if self.root is None:
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def height(self, AVLN: AVLNode):
        """
        Gets height of AVLN i.e. distance from it to the deepest node in its sub tree.
        :param AVLN: Starting Node
        :return: height
        """
        h = 0
        self.comparisons += 1
        if AVLN is not None:
            l_height = self.height(AVLN.left)
            r_height = self.height(AVLN.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

    def leftRotate(self, AVLN: AVLNode):
        """
        Rotates the tree starting from AVLNode to the left

        Rotations are explained further in the report.

        :param AVLN: Pivot point for rotation
        :return: Rotated sub tree
        """
        AVLNR = AVLN.right
        AVLNL = AVLNR.left
        AVLNR.left = AVLN
        AVLN.right = AVLNL
        self.rotations += 1
        return AVLNR

    def rightRotate(self, AVLN: AVLNode):
        """
        Rotates the tree starting from AVLNode to the right

        Rotations are explained further in the report.

        :param AVLN: Pivot point for rotation
        :return: Rotated sub tree
        """
        AVLNL = AVLN.left
        AVLNR = AVLNL.right
        AVLNL.right = AVLN
        AVLN.left = AVLNR
        self.rotations += 1
        return AVLNL

    def getBalance(self, AVLN: AVLNode):
        """
        Gets the balance of a sub tree
        :param AVLN: root of sub tree
        :return: balance: 0 if equal, negative if right sub tree is larger
        """
        if AVLN is None:
            return 0

        return self.height(AVLN.left) - self.height(AVLN.right)

    def _insert(self, AVLN: AVLNode, key):
        """
        Find appropriate location for key and then inserts it as a new AVLNode as a child for AVLN. Balancing is done
        after insertion.

        This function acts as a helper function to insert()

        :param AVLN: Would be parent of new node
        :param key: key value of new node
        :return: A balanced AVL Tree with key inserted as new AVLNode
        """

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

        # Get balancing
        bf = self.getBalance(AVLN)

        # Balance is further explained in the report
        # Case 1
        self.comparisons += 2
        if bf > 1 and key < AVLN.left.key:
            return self.rightRotate(AVLN)
        # Case 2
        self.comparisons += 2
        if bf < -1 and key > AVLN.right.key:
            return self.leftRotate(AVLN)
        # Case 3
        self.comparisons += 2
        if bf > 1 and key > AVLN.left.key:
            AVLN.left = self.leftRotate(AVLN.left)
            return self.rightRotate(AVLN)
        # Case 4
        self.comparisons += 2
        if bf < -1 and key < AVLN.right.key:
            AVLN.right = self.rightRotate(AVLN.right)
            return self.leftRotate(AVLN)

        return AVLN

    def insert(self, key):
        """
        Inserts key as an AVLNode in the tree
        :param key: key value of new node
        """
        self.comparisons += 1
        if self.root is None:
            self.root = AVLNode(key)
        else:
            self.root = self._insert(self.root, key)

    def getMinValueNode(self, root: AVLNode):
        """
        Finds the node with smallest key for a sub tree starting in root
        :param root: root of sub tree
        :return: AVLNode with smallest key value
        """
        self.comparisons += 1
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def _delete(self, AVLN: AVLNode, key):
        """
        Finds AVLNode with key as its key and deletes it. Balancing is done after deletion.

        This function acts as a helper function to delete()

        :param AVLN: Parent of the deleted node
        :param key: key value of the node that needs to be deleted
        :return: A balanced AVL Tree with node with key as its key removed
        """

        # Perform standard BST delete
        self.comparisons += 3
        if AVLN is None:
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

            temp = self.getMinValueNode(AVLN.left)
            AVLN.key = temp.key
            AVLN.left = self._delete(AVLN.left, temp.key)

        # Balancing
        bf = self.getBalance(AVLN)
        # Balance is further explained in the report
        # Case 1
        self.comparisons += 2
        if bf > 1 and self.getBalance(AVLN.left) >= 0:
            return self.rightRotate(AVLN)
        # Case 2
        self.comparisons += 2
        if bf < -1 and self.getBalance(AVLN.right) <= 0:
            return self.leftRotate(AVLN)
        # Case 3
        self.comparisons += 2
        if bf > 1 and self.getBalance(AVLN.left) < 0:
            AVLN.left = self.leftRotate(AVLN.left)
            return self.rightRotate(AVLN)
        # Case 4
        self.comparisons += 2
        if bf < -1 and self.getBalance(AVLN.right) > 0:
            AVLN.right = self.rightRotate(AVLN.right)
            return self.leftRotate(AVLN)

        return AVLN

    def delete(self, key):
        """
        Deletes the node with key from the tree
        :param key: key value of the node that needs to be deleted
        """
        self.nodes -= 1
        self.root = self._delete(self.root, key)

    def search(self, key, AVLN: AVLNode):
        """
        Searches for node with key as its key value
        :param key: key value of the node that needs to be found
        :param AVLN: root of current sub tree
        :return: AVLNode with key as its key
        """
        self.comparisons += 1
        if AVLN is None:
            return None

        self.comparisons += 3
        if AVLN.key == key:
            self.comparisons -= 2
            return AVLN
        elif AVLN.key > key:
            self.comparisons -= 1
            return self.search(key, AVLN.right)
        else:
            return self.search(key, AVLN.left)
