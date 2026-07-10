from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        length = 0
        current = head
        while current:
            current = current.next
            length += 1
        mid = length // 2
        current = head
        while mid > 0 and current:
            mid -= 1
            current = current.next

        return current
