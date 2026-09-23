class Solution:
    def solve(self, n):
        count = 0
        for i in range(1, n + 1):
            digit_sum = sum(int(ch) for ch in str(i))
            if digit_sum % 10 == i % 10:
                count += 1
        return count


if __name__ == "__main__":
    n = int(input())
    solution = Solution()
    print(solution.solve(n))
