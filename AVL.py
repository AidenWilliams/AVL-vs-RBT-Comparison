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


    def rr_rotation(self, parent: TN.TreeNode):
        child = parent.right
        parent.right = child.left
        child.left = parent
        return child

    def ll_rotation(self, parent: TN.TreeNode):
        child = parent.left
        parent.left = child.right
        child.right = parent
        return child

    def lr_rotation(self, parent: TN.TreeNode):
        child = parent.left
        parent.left = self.rr_rotation(child)
        return self.ll_rotation(parent)

    def rl_rotation(self, parent: TN.TreeNode):
        child = parent.right
        parent.right = self.ll_rotation(child)
        return self.rr_rotation(parent)

    def balance(self, tree: TN.TreeNode):
        bal_factor = self.difference(tree)
        if bal_factor > 1:
            if self.difference(tree.left) > 0:
                tree = self.ll_rotation(tree)
            else:
                tree = self.lr_rotation(tree)
        elif bal_factor < -1:
            if self.difference(tree.right) > 0:
                tree = self.rl_rotation(tree)
            else:
                tree = self.rr_rotation(tree)
        return tree

    def _insert(self, node, value):
        if node is None:
            return TN.TreeNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)

        elif value >= node.value:
            node.right = self._insert(node.right, value)

        return self.balance(node)

    def insert(self, value):
        if self.root is None:
            self.root = TN.TreeNode(value)
        else:
            self.root = self._insert(self.root, value)

    # returns node of node containing value if found
    def _find(self, node, value):
        if node is None:
            return None
        if value < node.value:
            return self._find(node.left, value)
        elif value > node.value:
            return self._find(node.right, value)
        elif value is node.value:
            return node

    # def _getMinValueNode(self, root):
    #     if root is None or root.left is None:
    #         return root
    #
    #     return self._getMinValueNode(root.left)
    #
    # def _delete(self, node, value):
    #     if node is None:
    #         return None
    #
    #     elif value < node.value:
    #         node.left = self._delete(node.left, value)
    #
    #     elif value > node.value:
    #         node.right = self._delete(node.right, value)
    #
    #     else:
    #         if node.left is None:
    #             return node.right
    #
    #         elif node.right is None:
    #             return node.left
    #
    #         temp = self._getMinValueNode(node.right)
    #         node.right = self._delete(temp.right, temp.value)
    #
    # def delete(self, *args):
    #     checklist = {v: False for v in args}
    #     for v in checklist:
    #         if checklist[v]:
    #             continue
    #
    #         node = self._find(self.root, v)
    #         children = node.traverse_prefix()[1:]
    #
    #         # Avoid inserting ones that will be deleted anyways
    #         safe_children = []
    #         for c in children:
    #             if c in checklist:
    #                 checklist[c] = True
    #             else:
    #                 safe_children.append(c)
    #
    #         self._delete(self.root, v)
    #         for child in safe_children:
    #             self.insert(child)
    #
    #     self.balance(self.root)

    def delete(self, node, value):
        if node is None:
            return None

        if value > node.value:
            node.right = self.delete(node.right, value)
        elif value < node.value:
            node.left = self.delete(node.left, value)
        else:
            if node.right is not None:
                temp = node.right

                while temp.left is not None:
                    temp = temp.left

                node.value = temp.value
                node.right = self.delete(node.right, node.value)
            else:
                return node.left

        node = self.balance(node)
        return node


def __test__():
    AVL = avl()
    # First insert into None node (create root)
    AVL.insert(10)
    AVL.insert(20)
    AVL.insert(30)
    AVL.insert(40)
    AVL.insert(50)
    AVL.insert(25)
    print(AVL)
    AVL.delete(AVL.root, 40)
    # AVL.root = AVL.balance(AVL.root)
    print("*****************************")
    print(AVL)
    AVL.insert(40)
    print("*****************************")
    print(AVL)


__test__()
#TODO: Get an algorithm and do this from scratch incl insertion