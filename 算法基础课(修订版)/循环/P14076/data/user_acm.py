class Solution:
    def solve(self, arr, l, r):
        # 请在这里实现
        return 0, []


if __name__ == "__main__":
    n = int(input())
    arr = list(map(int, input().split()))
    q = int(input())

    solution = Solution()
    for _ in range(q):
        l, r = map(int, input().split())
        max_value, indices = solution.solve(arr, l, r)
        print(max_value)
        print(" ".join(map(str, indices)))
