from typing import Optional
import collections


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if node is None:
            return None
        clones = {node: Node(val=node.val)}
        q = collections.deque([node])
        while q:
            u = q.pop()
            for v in u.neighbors:
                if v not in clones:
                    clones[v] = Node(v.val)
                    q.append(v)
                clones[u].neighbors.append(clones[v])
        return clones[node]
