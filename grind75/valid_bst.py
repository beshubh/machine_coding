from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        order = []

        def inner(tree):
            if tree is None:
                return
            inner(tree.left)
            order.append(tree.val)
            inner(tree.right)

        inner(root)
        if not order:
            return True
        for i in range(1, len(order)):
            if order[i] <= order[i - 1]:
                return False
        return True
