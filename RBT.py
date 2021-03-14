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

    def _insert(self, TN, data):
        # Standard BST insertion
        if TN is None:
            return TreeNode(data, colour=1)

        if data < TN.data:
            TN.left = self._insert(TN.left, data)
        else:
            TN.right = self._insert(TN.right, data)

    def insert(self, data):
        if self.root is None:
            self.root = TreeNode(data, colour=0)
        else:
            self.root = self._insert(self.root, data)

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
