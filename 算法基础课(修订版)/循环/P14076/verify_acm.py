class Solution:
    def solve(self, arr, l, r):
        l -= 1
        r -= 1
        max_value = arr[l]
        max_indices = [l + 1]
        for i in range(l + 1, r + 1):
            if arr[i] > max_value:
                max_value = arr[i]
                max_indices = [i + 1]
            elif arr[i] == max_value:
                max_indices.append(i + 1)
        return max_value, max_indices


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
