# -*- coding: utf-8 -*-
"""Generate 10 test cases for P5496. First 8 small, last 2 n=200."""
from __future__ import print_function

import os
import random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def is_unimodal(p, left, right):
    i = left
    while i < right and p[i] <= p[i + 1]:
        i += 1
    while i < right and p[i] >= p[i + 1]:
        i += 1
    return i == right


def min_cost(p):
    n = len(p)
    inf = 10**18
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for left in range(0, n - length + 1):
            right = left + length - 1
            best = inf
            if is_unimodal(p, left, right):
                best = (p[left] + p[right]) * length
            for t in range(left, right):
                cur = dp[left][t] + dp[t + 1][right] + p[t] * p[t + 1]
                if cur < best:
                    best = cur
            dp[left][right] = best
    return dp[0][n - 1]


def write_case(idx, n, p):
    assert len(p) == n
    inp = str(n) + "\n" + " ".join(str(x) for x in p)
    ans = str(min_cost(p)) + "\n"
    in_path = os.path.join(DATA, str(idx) + ".in")
    out_path = os.path.join(DATA, str(idx) + ".out")
    with open(in_path, "wb") as f:
        f.write(inp.encode("ascii"))
    with open(out_path, "wb") as f:
        f.write(ans.encode("ascii"))


def main():
    os.makedirs(DATA, exist_ok=True)
    random.seed(5496)

    # 1 样例1
    write_case(1, 3, [2, 3, 10])
    # 2 样例2
    write_case(2, 4, [3, 1, 4, 2])
    # 3 单点，代价 0
    write_case(3, 1, [7])
    # 4 两点：切开比直通便宜
    write_case(4, 2, [1, 100])
    # 5 全相等，单峰
    write_case(5, 6, [5, 5, 5, 5, 5, 5])
    # 6 严格递减单峰
    write_case(6, 8, [8, 7, 6, 5, 4, 3, 2, 1])
    # 7 山谷，必须切开
    write_case(7, 7, [9, 1, 8, 1, 7, 1, 6])
    # 8 小随机
    write_case(8, 12, [random.randint(1, 100) for _ in range(12)])
    # 9 最大规模随机
    write_case(9, 200, [random.randint(1, 100) for _ in range(200)])
    # 10 最大规模：交替高低，强迫多次切开
    p10 = []
    for i in range(200):
        p10.append(100 if i % 2 == 0 else 1)
    write_case(10, 200, p10)
    print("generated 10 cases")


if __name__ == "__main__":
    main()
