class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        """Return the FizzBuzz sequence from 1 through n."""
        result = []

        for number in range(1, n + 1):
            value = ""
            if number % 3 == 0:
                value += "Fizz"
            if number % 5 == 0:
                value += "Buzz"
            result.append(value or str(number))

        return result


if __name__ == "__main__":
    print(Solution().fizzBuzz(15))
