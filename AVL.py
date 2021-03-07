import TreeNode as TN


class avl(object):
    def __init__(self):
        self.root = None

    def __str__(self, node=None):
        if node is None:
            if self.is_empty():
                return 'root -> None'
            else:
                return '\n'.join(self.root.__str__(self.root))

    def is_empty(self):
        return self.root is None

    def height(self, tree: TN.TreeNode):
        h = 0
        if tree is not None:
            l_height = self.height(tree.left)
            r_height = self.height(tree.right)
            max_height = max(l_height, r_height)
            h = max_height + 1

        return h

    def difference(self, tree: TN.TreeNode):
        l_height = self.height(tree.left)
        r_height = self.height(tree.right)
        return l_height - r_height

    @staticmethod
    def rr_rotation(parent: TN.TreeNode):
        child = parent.right
        parent.right = child.left
        child.left = parent
        return child

    @staticmethod
    def ll_rotation(parent: TN.TreeNode):
        child = parent.left
        parent.left = child.right
        child.right = parent
        return child

    @staticmethod
    def lr_rotation(parent: TN.TreeNode):
        child = parent.left
        parent.left = avl.rr_rotation(child)
        return avl.ll_rotation(parent)

    @staticmethod
    def rl_rotation(parent: TN.TreeNode):
        child = parent.right
        parent.right = avl.ll_rotation(child)
        return avl.rr_rotation(parent)

    def balance(self, tree: TN.TreeNode):
        bal_factor = self.difference(tree)
        if bal_factor > 1:
            if self.difference(tree.left) > 0:
                tree = avl.ll_rotation(tree)
            else:
                tree = avl.lr_rotation(tree)
        elif bal_factor < -1:
            if self.difference(tree.right) > 0:
                tree = avl.rl_rotation(tree)
            else:
                tree = avl.rr_rotation(tree)
        return tree

    def _insert(self, tree, value):
        if tree is None:
            return TN.TreeNode(value)

        if value < tree.value:
            tree.left = self._insert(tree.left, value)

        elif value >= tree.value:
            tree.right = self._insert(tree.right, value)

        return self.balance(tree)

    def insert(self, value):
        if self.root is None:
            self.root = TN.TreeNode(value)
        else:
            self.root = self._insert(self.root, value)

    # TODO: Do delete function


def __test__():
    AVL = avl()
    # First insert into None node (create root)
    AVL.insert(10)
    AVL.insert(20)
    AVL.insert(30)
    AVL.insert(40)
    AVL.insert(50)
    AVL.insert(25)
    print(AVL.root.traverse_infix())
    print(AVL.root.traverse_prefix())
    print(AVL.root.traverse_postfix())
    print(AVL)


__test__()
