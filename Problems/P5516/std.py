# -*- coding: utf-8 -*-
"""P5516 最长山峰子序列"""


def longest_mountain(a):
    n = len(a)
    # left[i]：以 i 结尾的最长严格递增子序列长度
    left = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and left[j] + 1 > left[i]:
                left[i] = left[j] + 1
    # right[i]：以 i 开头的最长严格递减子序列长度
    right = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if a[j] < a[i] and right[j] + 1 > right[i]:
                right[i] = right[j] + 1
    ans = 0
    for i in range(n):
        # 峰顶左右都至少还要各有一个点，总长 >= 3
        if left[i] >= 2 and right[i] >= 2:
            ans = max(ans, left[i] + right[i] - 1)
    return ans


def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(longest_mountain(a))


if __name__ == "__main__":
    main()
