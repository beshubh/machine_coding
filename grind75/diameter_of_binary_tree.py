# Definition for a binary tree node.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        diameter = 0

        def dfs(tree):
            nonlocal diameter
            if tree is None:
                return 0
            left = dfs(tree.left)
            right = dfs(tree.right)
            # diameter might at this node: here if you think about it we are not using current node which means left + right is total number of edges
            diameter = max(diameter, left + right)
            # return maximum of left or right, choosing only one path as choosing both' won't constitute to a diameter
            # 1 here is for the current node height
            return 1 + max(left, right)

        dfs(root)
        return diameter
