def count_triplets(a, d):
    a.sort()
    n, ans = len(a), 0
    for i in range(n):
        r = n - 1
        while r > i + 1 and a[r] - a[i] > d:
            r -= 1
        while r > i + 1:
            ans += r - i - 1
    return ans




cmd = ['r', 'l', 'u', 'd', 'r', u]
M = 10

