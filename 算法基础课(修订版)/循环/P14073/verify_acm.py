class Solution:
    def solve(self, left_weights, right_weights):
        left_total = sum(left_weights)
        right_total = sum(right_weights)
        return "Equal" if left_total == right_total else "Not Equal"


if __name__ == "__main__":
    n, m = map(int, input().split())
    left_weights = list(map(int, input().split()))
    right_weights = list(map(int, input().split()))

    solution = Solution()
    result = solution.solve(left_weights, right_weights)

    print(result)
