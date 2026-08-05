import math


class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        level = 0
        n, m = len(matrix), len(matrix[0])
        result = []
        for level in range(math.ceil(min(n, m) / 2)):
            top = level
            bottom = n - 1 - level
            left = level
            right = m - 1 - level

            # top
            for j in range(left, right + 1):
                result.append(matrix[top][j])
            # right
            for i in range(top + 1, bottom + 1):
                result.append(matrix[i][right])

            # only one row remains
            if top == bottom:
                continue
            # bottom
            for j in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][j])

            # only one column remains
            if left == right:
                continue
            # left
            for i in range(bottom - 1, top, -1):
                result.append(matrix[i][left])
        return result
