class avl:
    def __init__(self):
        self.value = 0
        self.left = avl()
        self.right = avl()


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
        tree = parent.right
        parent.right = tree.left
        tree.left = parent
        return tree

    @staticmethod
    def ll_rotation(parent: avl):
        tree = parent.left
        parent.left = tree.right
        tree.right = parent
        return tree

    @staticmethod
    def lr_rotation(parent: avl):
        tree = parent.left
        parent.left = avl_tree.rr_rotation(tree)
        return avl_tree.ll_rotation(parent)

    @staticmethod
    def rl_rotation(parent: avl):
        tree = parent.right
        parent.right = avl_tree.ll_rotation(tree)
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

    def insert(self, tree: avl, value: int):
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

    def show(self, tree: avl, depth=1):
        if tree is not None:
            self.show(tree.right, depth + 1)
            print(" ")
            if tree is self.right:
                print("Root -> ")
            for i in range(depth):
                if tree is self.right:
                    break

                print(" " + str(tree.value))
                self.show(tree.left, depth + 1)

    def in_order(self, tree: avl):
        if tree is None:
            return
        self.in_order(tree.left)
        print(str(tree.value) + " ")
        self.in_order(tree.right)

    def pre_order(self, tree: avl):
        if tree is None:
            return

        print(str(tree.value) + " ")
        self.in_order(tree.left)
        self.in_order(tree.right)

    def post_order(self, tree: avl):
        if tree is None:
            return

        self.in_order(tree.left)
        self.in_order(tree.right)
        print(str(tree.value) + " ")