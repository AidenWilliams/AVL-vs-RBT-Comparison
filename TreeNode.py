class TreeNode(object):
    def __init__(self, data, left_child=None, right_child=None):
        self.data = data
        self.left = left_child
        self.right = right_child
        # ignored for avl trees
        self.color = 1  # 1 for red, 0 for black

    def __str__(self, node=None):
        if node is None:
            return '\n'.join(self.__str__(self))
        strings = []
        if node.right is not None:
            for right_string in self.__str__(node.right):
                strings.append(5 * ' ' + right_string.replace('->', '/-', 1))
        strings.append('-> ({})'.format(repr(node.data)))
        if node.left is not None:
            for left_string in self.__str__(node.left):
                strings.append(5 * ' ' + left_string.replace('->', '\\-', 1))
        return strings

    def traverse_infix(self, result=None):
        if result is None:
            result = []

        if self.left:
            self.left.traverse_infix(result)

        result.append(self.data)

        if self.right:
            self.right.traverse_infix(result)

        return result

    def traverse_prefix(self, result=None):
        if result is None:
            result = []

        result.append(self.data)

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

        result.append(self.data)

        return result
