class Solution:
    # Input: s = "([])"
    # stack = []
    def isValid(self, s: str) -> bool:

        stack = []
        for brace in s:
            match brace:
                case "(" | "[" | "{":
                    stack.append(brace)
                case ")" | "]" | "}":
                    if not stack:
                        return False
                    if (
                        (stack[-1] == "(" and brace == ")")
                        or (stack[-1] == "[" and brace == "]")
                        or (stack[-1] == "{" and brace == "}")
                    ):
                        stack.pop()
                    else:
                        return False
        return len(stack) == 0
