# Definition for a binary tree node.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":

        def inner(root):
            if p.val < root.val and q.val < root.val:
                return inner(root.left)
            if p.val > root.val and q.val > root.val:
                return inner(root.right)
            return root

        return inner(root)
