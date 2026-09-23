class Solution:
    def solve(self, n, k, intervals):
        # 请在这里实现
        return 0


if __name__ == "__main__":
    n, k = map(int, input().split())
    intervals = [list(map(int, input().split())) for _ in range(n)]

    solution = Solution()
    print(solution.solve(n, k, intervals))
