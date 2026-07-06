class Solution:
    # Input: [7, 1, 5, 3, 6, 4]
    # max = 7, min = 7
    # min = 1, max = 1
    # 1, 5 => 4
    # 1, 6 => 5
    # 1, 4
    def maxProfit(self, prices: list[int]) -> int:
        min_price = prices[0]
        max_price = prices[0]
        max_profit = 0
        for p in prices:
            if min_price > p:
                min_price = p
                max_price = p
            max_price = max(max_price, p)
            max_profit = max(max_profit, max_price - min_price)
        return max_profit
