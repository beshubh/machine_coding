import collections


class DSU:
    def __init__(self, nodes) -> None:
        self._root = {n: n for n in nodes}
        self._rank = {n: 0 for n in nodes}

    def find(self, node):
        if self._root[node] != node:
            self._root[node] = self.find(self._root[node])
        return self._root[node]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        rankx, ranky = self._rank[rx], self._rank[ry]
        if rankx < ranky:
            rankx, ranky = ranky, rankx
        self._root[ry] = rx
        if rankx == ranky:
            self._rank[rx] += 1
        return True


class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        email_name_map = {}
        emails = []
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                email_name_map[email] = name
                emails.append(email)

        dsu = DSU(emails)

        for account in accounts:
            main = account[1]
            for res in account[2:]:
                dsu.union(main, res)

        cluster = collections.defaultdict(set)
        for email in emails:
            p = dsu.find(email)
            cluster[p].add(email)

        result = []
        for k, v in cluster.items():
            temp = []
            temp.append(email_name_map[k])
            temp.extend(sorted(v))
            result.append(temp)
        return res
