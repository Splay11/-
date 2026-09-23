# -*- coding: utf-8 -*-
"""Generate 10 test cases for P5496. First 8 small, last 2 n=1e5."""
from __future__ import print_function

import os
import random
import string

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def distinct_count(s):
    seen = [False] * 26
    tot = 0
    for ch in s:
        idx = ord(ch) - 97
        if not seen[idx]:
            seen[idx] = True
            tot += 1
    return tot


def can_split(s, m, limit):
    n = len(s)
    pieces = 0
    i = 0
    while i < n:
        pieces += 1
        if pieces > m:
            return False
        cnt = [0] * 26
        kinds = 0
        j = i
        while j < n:
            idx = ord(s[j]) - 97
            if cnt[idx] == 0:
                if kinds == limit:
                    break
                kinds += 1
            cnt[idx] += 1
            j += 1
        if j == i:
            return False
        i = j
    return True


def min_interference(s, m):
    left = 1
    right = distinct_count(s)
    while left < right:
        mid = (left + right) // 2
        if can_split(s, m, mid):
            right = mid
        else:
            left = mid + 1
    return left


def brute(s, m):
    n = len(s)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        seen = [False] * 26
        kinds = 0
        for j in range(i, n):
            idx = ord(s[j]) - 97
            if not seen[idx]:
                seen[idx] = True
                kinds += 1
            dist[i][j] = kinds
    inf = 99
    dp = [[inf] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for k in range(1, min(i, m) + 1):
            best = inf
            for j in range(k - 1, i):
                cur = dp[j][k - 1]
                if cur == inf:
                    continue
                val = cur if cur > dist[j][i - 1] else dist[j][i - 1]
                if val < best:
                    best = val
            dp[i][k] = best
    return dp[n][m]


def write_case(idx, n, m, s):
    assert len(s) == n
    inp = str(n) + " " + str(m) + "\n" + s
    ans = str(min_interference(s, m)) + "\n"
    if n <= 20:
        b = brute(s, m)
        assert b == min_interference(s, m), (s, m, b, min_interference(s, m))
    with open(os.path.join(DATA, str(idx) + ".in"), "wb") as f:
        f.write(inp.encode("ascii"))
    with open(os.path.join(DATA, str(idx) + ".out"), "wb") as f:
        f.write(ans.encode("ascii"))


def main():
    os.makedirs(DATA, exist_ok=True)
    random.seed(54960)

    # 1 样例1
    write_case(1, 5, 2, "aabbc")
    # 2 样例2
    write_case(2, 6, 3, "abcabc")
    # 3 单字符
    write_case(3, 1, 1, "z")
    # 4 全相同，答案 1
    write_case(4, 8, 3, "aaaaaaaa")
    # 5 m=n，答案 1
    write_case(5, 7, 7, "abcdefg")
    # 6 m=1，答案为整串种类数
    write_case(6, 10, 1, "abacabadac")
    # 7 小随机，与暴力对拍
    s7 = "".join(random.choice("abcde") for _ in range(16))
    write_case(7, 16, 5, s7)
    # 8 交替字母，卡均分长度
    write_case(8, 12, 4, "abababababab")
    # 9 最大规模随机
    s9 = "".join(random.choice(string.ascii_lowercase) for _ in range(100000))
    write_case(9, 100000, 100, s9)
    # 10 最大规模：周期 26 字母，m 较小
    alphabet = string.ascii_lowercase
    s10 = (alphabet * (100000 // 26 + 1))[:100000]
    write_case(10, 100000, 50, s10)
    print("generated 10 cases")


if __name__ == "__main__":
    main()
