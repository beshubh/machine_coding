#include <vector>

class Solution {
    using BoardT = std::vector<std::vector<long long>>;
    static bool inside(int row, int col, int rows, int cols) {
        return row >= 0 && row < rows && col >= 0 && col < cols;
    }

    static int countDirection(const BoardT &board, int row, int col, int rowChange, int colChange,
                              long long token) {
        const int rows = static_cast<int>(board.size());
        const int cols = static_cast<int>(board[0].size());
        int count = 0;

        row += rowChange;
        col += colChange;
        while (inside(row, col, rows, cols) && board[row][col] == token) {
            count += 1;
            row += rowChange;
            col += colChange;
        }
        return count;
    }

  public:
    bool winning_move(const std::vector<std::vector<long long>> board, int row, int col, int k) {
        const long long token = board[row][col];
        if (token == 0) {
            return false;
        }
        const int directions[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};

        for (const auto &dir : directions) {
            const int dr = dir[0];
            const int dc = dir[1];
            int consecutive = 1;
            consecutive += countDirection(board, row, col, dr, dc, token);
            consecutive += countDirection(board, row, col, -dr, -dc, token);
            if (consecutive >= k) {
                return true;
            }
        }
        return false;
    }
};
