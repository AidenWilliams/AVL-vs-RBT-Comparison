class avl:
    def __init__(self):
        self.value = 0
        self.left = None
        self.right = None

    # Thank you to Alan Davis for this print string function
    def __str__(self, node=None):
        if node is None:
            return '\n'.join(self.__str__(self))
        strings = []
        if node.right is not None:
            for right_string in self.__str__(node.right):
                strings.append(5 * ' ' + right_string.replace('->', '/-', 1))
        strings.append('-> ({})'.format(repr(node.value)))
        if node.left is not None:
            for left_string in self.__str__(node.left):
                strings.append(5 * ' ' + left_string.replace('->', '\\-', 1))
        return strings


class avl_tree:
    def __init__(self):
        self.root = avl()

    def __str__(self, node=None):
        if node is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def height(self, tree: avl):
        h = 0
        if tree is not None:
            l_height = self.height(tree.left)
            r_height = self.height(tree.right)
            max_height = max(l_height, r_height)
            h = max_height + 1

        return h

    def difference(self, tree: avl):
        l_height = self.height(tree.left)
        r_height = self.height(tree.right)
        return l_height - r_height

    @staticmethod
    def rr_rotation(parent: avl):
        child = parent.right
        parent.right = child.left
        child.left = parent
        return child

    @staticmethod
    def ll_rotation(parent: avl):
        child = parent.left
        parent.left = child.right
        child.right = parent
        return child

    @staticmethod
    def lr_rotation(parent: avl):
        child = parent.left
        parent.left = avl_tree.rr_rotation(child)
        return avl_tree.ll_rotation(parent)

    @staticmethod
    def rl_rotation(parent: avl):
        child = parent.right
        parent.right = avl_tree.ll_rotation(child)
        return avl_tree.rr_rotation(parent)

    def balance(self, tree: avl):
        bal_factor = self.difference(tree)
        if bal_factor > 1:
            if self.difference(tree.left) > 0:
                tree = avl_tree.ll_rotation(tree)
            else:
                tree = avl_tree.lr_rotation(tree)
        elif bal_factor < -1:
            if self.difference(tree.right) > 0:
                tree = avl_tree.rl_rotation(tree)
            else:
                tree = avl_tree.rr_rotation(tree)
        return tree

    @staticmethod
    def insertRoot(value: int):
        tree = avl()
        tree.value = value
        tree.left = None
        tree.right = None
        return tree

    def insert(self, tree, value: int):
        if tree is None:
            tree = avl()
            tree.value = value
            tree.left = None
            tree.right = None
            return tree
        elif value < tree.value:
            tree.left = self.insert(tree.left, value)
        elif value >= tree.value:
            tree.right = self.insert(tree.right, value)
        return self.balance(tree)

    #

    def in_order(self, tree: avl):
        if tree is None:
            return

        self.in_order(tree.left)
        print(str(tree.value) + " ", end="")
        self.in_order(tree.right)

    def pre_order(self, tree: avl):
        if tree is None:
            return

        print(str(tree.value) + " ", end="")
        self.pre_order(tree.left)
        self.pre_order(tree.right)

    def post_order(self, tree: avl):
        if tree is None:
            return

        self.post_order(tree.left)
        self.post_order(tree.right)
        print(str(tree.value) + " ", end="")

    #TODO: Do delete function

def __test__():
    avlTree = avl_tree()
    # First insert into None node (create root)
    root = avlTree.insertRoot(3)
    root = avlTree.insert(root, 2)
    root = avlTree.insert(root, 1)
    root = avlTree.insert(root, 4)
    root = avlTree.insert(root, 5)
    root = avlTree.insert(root, 6)
    root = avlTree.insert(root, 7)
    root = avlTree.insert(root, 16)
    root = avlTree.insert(root, 15)
    root = avlTree.insert(root, 14)
    avlTree.in_order(root)
    print("")
    avlTree.pre_order(root)
    print("")
    avlTree.post_order(root)
    print("")
    print(root)


# __test__()
