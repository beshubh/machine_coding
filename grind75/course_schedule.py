import collections


class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        graph = {n: [] for n in range(numCourses)}
        indegree = {n: 0 for n in graph.keys()}
        for pa, pb in prerequisites:
            indegree[pa] += 1
            graph[pb].append(pa)

        q = collections.deque([node for node in indegree.keys() if indegree[node] == 0])
        topo_order = []
        while q:
            u = q.popleft()
            topo_order.append(u)
            for v in graph[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)
        return len(topo_order) == numCourses
