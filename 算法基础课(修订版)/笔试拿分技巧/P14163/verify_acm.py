class Solution:
    def solve(self, a):
        return " ".join(str(x) for x in a)


if __name__ == "__main__":
    n = int(input())
    a = list(map(int, input().split()))

    solution = Solution()
    print(solution.solve(a), end="")
