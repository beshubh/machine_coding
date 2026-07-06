from typing import Optional
import collections


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        dummy = root
        q = collections.deque([root])
        while q:
            parent = q.pop()
            if not parent:
                continue
            parent.left, parent.right = parent.right, parent.left
            q.appendleft(parent.left)
            q.appendleft(parent.right)
        return dummy
