class Solution:
    def solve(self, arr):
        # 请在这里实现
        return 0, []


if __name__ == "__main__":
    n = int(input())
    arr = list(map(int, input().split()))

    solution = Solution()
    max_value, indices = solution.solve(arr)

    print(max_value)
    print(" ".join(map(str, indices)))
