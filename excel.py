from dataclasses import dataclass
import collections


@dataclass
class Cell:
    is_formula: bool = False
    value: int = 0


class Excel:
    def __init__(self, height: int, width: str) -> None:
        self._height = height + 1
        self._width = ord(width) - ord('A') + 2
        self._grid = [
            [Cell() for _ in range(self._width)]
            for _ in range(self._height)
        ]
        # contains depdenency relations from source cells -> target
        # if the source cell contributes to the sum of the target cell
        # (r, c) -> { (tr, tc)}
        self._dependents: dict[tuple[int, int], set] = collections.defaultdict(set)
        # contains all the cells that some `target` cell T depends on for sum calculation
        # (tr, tc) -> { (ri, ci): count}
        self._formula: dict[tuple[int, int], collections.Counter] = {}


    def _get_col(self, column: str) -> int:
        return ord(column) - ord('A') + 1

    def _clear_formula(self, cell):
        if cell not in self._formula:
            return
        for source in self._formula[cell].keys():
            self._dependents[source].discard(cell)
        r, c = cell
        self._grid[r][c].is_formula = False
        del self._formula[cell]

    def _cell_value(self, cell) -> int:
        r, c = cell
        return self._grid[r][c].value

    def _compute_formula_values(self, cell):
        total = 0
        for source, cnt in self._formula[cell].items():
            total += self._cell_value(source) * cnt
        return total

    def _propogate_formula(self, cell):
        order = []
        seen = set()

        def dfs(u):
            for v in self._dependents[u]:
                if v in seen:
                    continue
                seen.add(v)
                dfs(v)
                order.append(v)

        dfs(cell)
        # target node will be at last after dfs in `order`
        for dependent in reversed(order):
            r, c = dependent
            self._grid[r][c].value = self._compute_formula_values(dependent)

    def set(self, row, column: str, val: int) -> None:
        col = self._get_col(column)
        cell = (row, col)
        self._clear_formula(cell)
        # 1st: row, col is emtpy or have a vlaue
        # 2nd: row, col have a formula
        self._grid[row][col].value = val
        self._grid[row][col].is_formula = False
        self._propogate_formula(cell)

    def get(self, row, column: str) -> int:
        col = self._get_col(column)
        return self._cell_value((row, col))


    def _parse_numbers(self, numbers: list[str]) -> collections.Counter:
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
                start_row = int(start[1:])
                start_col = self._get_col(start[0])
                end_row = int(end[1:])
                end_col = self._get_col(end[0])
                for r in range(start_row, end_row + 1):
                    for c in range(start_col, end_col + 1):
                        refs[(r, c)] += 1
            else:
                raise ValueError('Invalid range')
        return refs

    def sum(self, row, column: str, numbers: list[str]) -> int:
        col = self._get_col(column)
        cell = (row, col)
        self._clear_formula(cell)
        refs = self._parse_numbers(numbers)
        self._formula[cell] = refs
        for source in refs:
            self._dependents[source].add(cell)
        self._grid[row][col].value = self._compute_formula_values(cell)
        self._grid[row][col].is_formula = True
        self._propogate_formula(cell)
        return self._cell_value(cell)

