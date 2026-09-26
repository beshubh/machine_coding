class Solution:
    def validate_subbox(self, r, re, c, ce, board):
        seen = set()
        for i in range(r, re):
            for j in range(c, ce):
                cell = board[i][j]
                if cell == ".":
                    continue
                elif int(cell) not in range(1, 10) or cell in seen:
                    return False
                else:
                    seen.add(cell)
        return True

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        for row in board:
            seen = set()
            for v in row:
                if v == ".":
                    continue
                elif int(v) not in range(1, 10) or v in seen:
                    return False
                else:
                    seen.add(v)

        for c in range(len(board[0])):
            seen = set()
            for r in range(len(board)):
                cell = board[r][c]
                if cell == ".":
                    continue
                elif int(cell) not in range(1, 10) or cell in seen:
                    return False
                else:
                    seen.add(cell)

        for r in range(0, len(board), 3):
            for c in range(0, len(board[0]), 3):
                if not self.validate_subbox(r, r + 3, c, c + 3, board):
                    return False
        return True
