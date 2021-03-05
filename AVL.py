class avl:
    def __init__(self):
        self.value = 0
        self.left = None
        self.right = None


class avl_tree:
    def __init__(self):
        self.root = avl()

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

    # TODO: Fix show and order functions
    def show(self, tree: avl, depth=1):
        if tree is not None:
            self.show(tree.right, depth + 1)
            print(" ", end="")
            if tree is self.root:
                print("Root -> ", end="")
            for i in range(depth):
                if tree is self.root:
                    break

                print(" " + str(tree.value), end="")
                self.show(tree.left, depth + 1)

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
        self.in_order(tree.left)
        self.in_order(tree.right)

    def post_order(self, tree: avl):
        if tree is None:
            return

        self.in_order(tree.left)
        self.in_order(tree.right)
        print(str(tree.value) + " ", end="")


def __test__():
    avlTree = avl_tree()
    # First insert into None node (create root)
    r = avlTree.insert(None, 13)
    r = avlTree.insert(r, 10)
    r = avlTree.insert(r, 15)
    r = avlTree.insert(r, 5)
    r = avlTree.insert(r, 11)
    r = avlTree.insert(r, 4)
    r = avlTree.insert(r, 8)
    r = avlTree.insert(r, 16)
    # avlTree.in_order(r)
    # print("")
    # avlTree.pre_order(r)
    # print("")
    # avlTree.post_order(r)
    # print("")

    avlTree.show(r)


__test__()
