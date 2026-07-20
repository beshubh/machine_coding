class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        output = []
        current = []
        n = len(candidates)

        def go(i: int, acc: int):
            if i >= n:
                return
            if acc == target:
                output.append(current.copy())
                return
            if acc > target:
                return
            # take and skip
            current.append(candidates[i])
            go(i, acc + candidates[i])
            current.pop()
            go(i + 1, acc)

        go(0, 0)
        return output
