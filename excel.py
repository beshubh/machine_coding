from dataclasses import dataclass
from typing import List
import collections


@dataclass()
class Cell:
    is_formula: bool = False
    value: int  = 0

class Excel:

    def __init__(self, height: int, width: str):
        self._height = height + 1
        self._width = ord(width) - ord('A') + 2
        # height is 1 more so we start at 0
        self._grid = [
            [Cell() for _ in range(self._width)]
            for _ in range(self._height)
        ]
        self._dependents = collections.defaultdict(set)
        self._formula = {}

    def _get_col(self, column: str) -> int:
        return ord(column) - ord('A') + 1
    
    def _cell_value(self, cell):
        r, c = cell
        return self._grid[r][c].value
    
    def _clear_formula(self, cell):
        if cell not in self._formula:
            return
        for source in self._formula[cell]:
            self._dependents[source].discard(cell)
        del self._formula[cell]
        r, c = cell
        self._grid[r][c].is_formula = False

    def _compute_formula_values(self, cell):
        total = 0
        for source, cnt in self._formula[cell].items():
            total += self._cell_value(source) * cnt
        return total

    def _propogate_form(self, cell):
        seen = set()
        order = []
        def dfs(u):
            for v in self._dependents[u]:
                if v in seen:
                    continue
                seen.add(v)
                dfs(v)
                order.append(v)
        dfs(cell)
        for dependent in reversed(order):
            r, c = dependent
            self._grid[r][c].value = self._compute_formula_values(dependent)

    def _parse_numbers(self, numbers: list[str]):
        refs = collections.Counter()
        for entry in numbers:
            parts = entry.split(':')
            if len(parts) == 1:
                ref = parts[0]
                col = self._get_col(ref[0])
                row = int(ref[1:])
                refs[(row, col)] += 1
            elif len(parts) == 2:
                start, end = parts
                start_col = self._get_col(start[0])
                start_row = int(start[1:])
                end_col = self._get_col(end[0])
                end_row = int(end[1:])
                for r in range(start_row, end_row + 1):
                    for c in range(start_col, end_col + 1):
                        refs[(r, c)] += 1
            else:
                raise ValueError('Invalid formula range')
        return refs

    def set(self, row: int, column: str, val: int) -> None:
        col = self._get_col(column)
        cell = (row, col)
        self._clear_formula(cell)
        self._grid[row][col].value = val
        self._grid[row][col].is_formula = False
        self._propogate_form(cell)

    def get(self, row: int, column: str) -> int:
        col = self._get_col(column)
        return self._grid[row][col].value

    def sum(self, row: int, column: str, numbers: List[str]) -> int:
        col = self._get_col(column)
        cell = (row, col)
        self._clear_formula(cell)
        refs = self._parse_numbers(numbers)
        self._formula[cell] = refs
        for source in refs:
            self._dependents[source].add(cell)
        self._grid[row][col].is_formula = True
        self._grid[row][col].value = self._compute_formula_values(cell)
        self._propogate_form(cell)
        return self._grid[row][col].value

# Your Excel object will be instantiated and called as such:
# obj = Excel(height, width)
# obj.set(row,column,val)
# param_2 = obj.get(row,column)
# param_3 = obj.sum(row,column,numbers)
