class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:

        def inner(i: int, s: int):
            if s == amount:
                return 0
            if i > len(coins):
                return float("inf")
            # choose
            a = 1 + inner(i, s + coins[i])
            b = inner(i + 1, s)
            return min(a, b)

        INF = float("inf")
        # minimum amount of coins needed to reach `amount` from current sum `am` using coins i .. n - 1
        dp = [[INF] * (amount + 1) for _ in range(len(coins) + 1)]
        for i in range(len(coins) + 1):
            # amount is already reached
            dp[i][amount] = 0

        for i in range(len(coins) - 1, -1, -1):
            for sm in range(amount, -1, -1):
                # minimum coins needed to reach `amount` from `sm`
                if sm + coins[i] <= amount:
                    dp[i][sm] = min(1 + dp[i][sm + coins[i]], dp[i + 1][sm])
                else:
                    dp[i][sm] = dp[i + 1][sm]
        return dp[0][0]  # type: ignore
