from typing import Optional
from heapq import heappush, heappop


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __lt__(self, other):
        return self.val < other.val


class Solution:
    # list1 => a -> b -> c
    # list2 => g -> h -> i
    # dummy = (nil) => a
    # heap = (a, b)
    # current = heap.pop()
    # loop
    #   push to heap list1, list2
    #
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        if list1 is None and list2 is None:
            return None

        if list1 is None:
            return list2
        if list2 is None:
            return list1
        seq = 0
        dummy = ListNode()
        pq = []
        heappush(pq, (list1.val, seq, list1))
        seq += 1
        list1 = list1.next
        heappush(pq, (list2.val, list2))
        seq += 1
        list2 = list2.next
        current = heappop(pq)[1]
        dummy.next = current
        current = current.next
        while pq:
            if list1:
                heappush(pq, (list1.val, seq, list1))
                list1 = list1.next
                seq += 1
            if list2:
                heappush(pq, (list2.val, seq, list2))
                list2 = list2.next
                seq += 1
            current.next = heappop(pq)[1]
            current = current.next
        return dummy.next


class Solution2:
    # list1 => a -> b -> c
    # list2 => g -> h -> i
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        if list1 is None and list2 is None:
            return None
        if list1 is None:
            return list2
        if list2 is None:
            return list1
        dummy = ListNode()
        if list1.val <= list2.val:
            dummy.next = list1
        else:
            dummy.next = list2
        current = dummy.next
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                current = current.next
                list1 = list1.next
            else:
                current.next = list2
                current = current.next
                list2 = list2.next

        while list1:
            current.next = list1
            current = current.next
            list1 = list1.next
        while list2:
            current.next = list2
            current = current.next
            list2 = list2.next

        return dummy.next
