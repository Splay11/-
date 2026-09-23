class Solution:
    def solve(self, arr):
        max_value = max(arr)
        indices = [i for i, v in enumerate(arr) if v == max_value]
        return max_value, indices


if __name__ == "__main__":
    n = int(input())
    arr = list(map(int, input().split()))

    solution = Solution()
    max_value, indices = solution.solve(arr)

    print(max_value)
    print(" ".join(map(str, indices)))
