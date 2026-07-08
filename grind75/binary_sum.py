class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        answer = []
        carry = 0
        while i >= 0 and j >= 0:
            if a[i] == b[j]:
                if a[i] == "1":
                    if carry == 1:
                        answer.append(1)
                        carry = 1
                    else:
                        answer.append(0)
                        carry = 1
                else:
                    if carry == 1:
                        answer.append(1)
                    else:
                        answer.append(0)
                    carry = 0
            else:
                if carry == 1:
                    answer.append(0)
                    carry = 1
                else:
                    answer.append(1)
            i -= 1
            j -= 1

        while i >= 0:
            if carry == 1:
                if a[i] == "1":
                    answer.append(0)
                    carry = 1
                else:
                    answer.append(1)
                    carry = 0
            else:
                answer.append(a[i])
            i -= 1

        while j >= 0:
            if carry == 1:
                if b[j] == "1":
                    answer.append(0)
                    carry = 1
                else:
                    answer.append(1)
                    carry = 0
            else:
                answer.append(b[j])
            j -= 1

        if carry == 1:
            answer.append(1)
        return "".join([str(s) for s in answer[::-1]])
