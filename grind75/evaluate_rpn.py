class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for token in tokens:
            match token:
                case "+":
                    stack.append(stack.pop() + stack.pop())
                case "-":
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(left - right)
                case "*":
                    stack.append(stack.pop() * stack.pop())
                case "/":
                    divisor = stack.pop()
                    dividend = stack.pop()
                    stack.append(int(dividend / divisor))
                case _:
                    stack.append(int(token))
        return stack[-1]
