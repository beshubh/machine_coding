import collections


class DSU:
    def __init__(self, nodes):
        self.root = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}

    def find(self, a):
        if self.root[a] != a:
            self.root[a] = self.find(self.root[a])
        return self.root[a]

    def union(self, a, b):
        roota, rootb = self.find(a), self.find(b)
        if roota == rootb:
            return False
        ranka, rankb = self.rank[roota], self.rank[rootb]
        if ranka < rankb:
            roota, rootb = rootb, roota
        self.root[rootb] = roota
        if ranka == rankb:
            self.rank[roota] += 1
        return True


class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        emails_map = {}
        all_emails = []
        for acc in accounts:
            name = acc[0]
            for i in range(1, len(acc)):
                email = acc[i]
                emails_map[email] = name
                all_emails.append(email)

        dsu = DSU(all_emails)
        for acc in accounts:
            first_email = acc[1]
            for i in range(2, len(acc)):
                rest = acc[i]
                dsu.union(first_email, rest)

        results = collections.defaultdict(set)
        for email in all_emails:
            results[dsu.find(email)].add(email)

        groups = []
        for _, emails in results.items():
            emails = sorted(list(emails))
            groups.append([emails_map[emails[0]], *emails])
        return groups
