# -*- coding: utf-8 -*-
"""P5332 造数：定长窗和模 0 的最小补量。"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from std import solve

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def write_file(idx, q, w, v):
    k = len(v)
    assert 1 <= k <= 500 and 1 <= q <= 500
    assert 1 <= w <= k
    for x in v:
        assert 0 <= x < q
    lines = ["%d %d %d" % (k, q, w), " ".join(str(x) for x in v)]
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(k, q, w, v)) + "\n")


def main():
    rng = random.Random(5332)
    write_file(1, 4, 2, [1, 1, 1])
    write_file(2, 3, 1, [0])
    write_file(3, 6, 2, [1, 2, 3, 4])
    # 4 窗长 1：每格单独补齐
    write_file(4, 5, 1, [1, 2, 3, 4, 0])
    # 5 整段一个窗
    write_file(5, 7, 6, [1, 2, 3, 4, 5, 6])
    # 6 已经全合法
    write_file(6, 4, 2, [0, 0, 0, 0])
    # 7 随机小
    k, q, w = 12, 9, 4
    v = [rng.randint(0, q - 1) for _ in range(k)]
    write_file(7, q, w, v)
    # 8 读数贴着定额-1，hack 只补第一窗
    write_file(8, 8, 3, [7, 7, 7, 7, 7, 7])
    # 9 中等 DP
    k, q, w = 200, 80, 40
    v = [rng.randint(0, q - 1) for _ in range(k)]
    write_file(9, q, w, v)
    # 10 上限附近
    k, q, w = 500, 200, 80
    v = [rng.randint(0, q - 1) for _ in range(k)]
    write_file(10, q, w, v)


if __name__ == "__main__":
    main()
