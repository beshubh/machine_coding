from typing import Optional
import collections


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:
        if not root:
            return []
        q = collections.deque([root])
        level_order = []
        while q:
            qlen = len(q)
            level = []
            for _ in range(qlen):
                current = q.pop()
                if current is None:
                    continue
                level.append(current.val)
                q.appendleft(current.left)
                q.appendleft(current.right)
            if level:
                level_order.append(level)
        return level_order
