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
        node = parent.right
        parent.right = node.left
        node.left = parent
        return node

    @staticmethod
    def ll_rotation(parent: avl):
        node = parent.left
        parent.left = node.right
        node.right = parent
        return node

    @staticmethod
    def lr_rotation(parent: avl):
        node = parent.left
        parent.left = avl_tree.rr_rotation(node)
        return avl_tree.ll_rotation(parent)

    @staticmethod
    def rl_rotation(parent: avl):
        node = parent.right
        parent.right = avl_tree.ll_rotation(node)
        return avl_tree.rr_rotation(parent)


'''avl *avl_tree::lr_rotat(avl *parent) {
   avl *t;
   t = parent->l;
   parent->l = rr_rotat(t);
   cout<<"Left-Right Rotation";
   return ll_rotat(parent);
}'''
