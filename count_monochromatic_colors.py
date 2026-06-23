

def count_monochromatic(grid: list[str]):
    dp = [[0] * len(grid[0]) for _ in range(len(grid))]
    ans = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            ans += 1 # every cell contributes
            if i > 0 and j > 0:
                c = grid[i][j]
                if grid[i - 1][j] == grid[i][j - 1] and grid[i - 1][j] == grid[i - 1][j - 1] and grid[i - 1][j - 1] == c:
                    dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])
                    ans += dp[i][j]

    return ans


def solution(grid):
    return count_monochromatic(grid)



if __name__ == '__main__':
    print(count_monochromatic(["aab", "aab", "bbb"]))
