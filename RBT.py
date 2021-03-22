from TreeNode import TreeNode


class RBT(object):
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

    def height(self, TN: TreeNode):
        h = 0
        if TN is not None:
            l_height = self.height(TN.left)
            r_height = self.height(TN.right)
            max_height = max(l_height, r_height)
            h = max_height + 1
        return h

    def getBalance(self, TN: TreeNode):
        if not TN:
            return 0

        return self.height(TN.left) - self.height(TN.right)

    def _insert(self, TN: TreeNode, data, path):
        # Standard BST insertion
        if TN is None:
            # Check for red children
            for node in path:
                if node.redChildren():
                    # flip colours
                    node.colour = 1
                    node.left.colour = 0
                    node.right.colour = 0

            return TreeNode(data, colour=1)

        if data < TN.data:
            TN.left = self._insert(TN.left, data, path+[TN])
        else:
            TN.right = self._insert(TN.right, data, path+[TN])


        # # Balancing
        # balance = self.getBalance(TN)
        #
        # if balance > 1 and data < TN.left.data:
        #     return self.rightRotate(TN)
        #
        # if balance < -1 and data > TN.right.data:
        #     return self.leftRotate(TN)
        #
        # if balance > 1 and data > TN.left.data:
        #     TN.left = self.leftRotate(TN.left)
        #     return self.rightRotate(TN)
        #
        # if balance < -1 and data < TN.right.data:
        #     TN.right = self.rightRotate(TN.right)
        #     return self.leftRotate(TN)
        #
        return TN

    def insert(self, data):
        if self.root is None:
            self.root = TreeNode(data, colour=0)
        else:
            self.root = self._insert(self.root, data, [self.root])

    def _delete(self, TN, data):
        # Perform standard BST delete
        if not TN:
            return TN

        elif data < TN.data:
            TN.left = self._delete(TN.left, data)

        elif data > TN.data:
            TN.right = self._delete(TN.right, data)

    def delete(self, *args):
        if type(args[0]) == list:  # otherwise it is given as a tuple
            args = args[0]
        for data in args:
            self.root = self._delete(self.root, data)

    @staticmethod
    def leftRotate(TN):
        #TN.colour = 1
        TN1 = TN.right
        TN2 = TN1.left
        TN1.left = TN
        TN.right = TN2
        #TN1.colour = 0
        return TN1

    @staticmethod
    def rightRotate(TN):
        #TN.colour = 1
        TN1 = TN.left
        TN2 = TN1.right
        TN1.right = TN
        TN.left = TN2
        #TN1.colour = 0
        return TN1

def __test__():
    rbt = RBT()
    # First insert into None node (create root)
    rbt.insert(10)
    rbt.insert(20)
    rbt.insert(30)
    rbt.insert(40)
    rbt.insert(25)
    rbt.insert(50)
    print(rbt)
    #print("*****************************")
    #avl.delete(40, 50)
    #print(avl)
    #print("*****************************")
    # AVL.delete(50)
    # # AVL.root = AVL.balance(AVL.root)

    #print(avl)
    # print(AVL)
    # AVL.insert(40)
    # print("*****************************")
    # print(AVL)


__test__()
