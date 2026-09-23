class Solution:
    def solve(self, left_weights, right_weights):
        # 请在这里实现
        return ""


if __name__ == "__main__":
    n, m = map(int, input().split())
    left_weights = list(map(int, input().split()))
    right_weights = list(map(int, input().split()))

    solution = Solution()
    result = solution.solve(left_weights, right_weights)

    print(result)
