# -*- coding: utf-8 -*-
"""P5331 造数：模和最小配对。"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from std import solve

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def write_file(idx, q, x, y):
    k = len(x)
    assert k == len(y)
    assert 1 <= k <= 300000
    assert 1 <= q <= 1000000000
    for a in x + y:
        assert 0 <= a < q
    lines = ["%d %d" % (k, q), " ".join(str(a) for a in x), " ".join(str(a) for a in y)]
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(k, q, x, y)) + "\n")


def main():
    rng = random.Random(5331)
    write_file(1, 5, [4, 0, 1], [1, 4, 2])
    write_file(2, 10, [3], [4])
    write_file(3, 7, [1, 2, 3, 6], [1, 1, 4, 5])
    # 4 全小，无法进位
    write_file(4, 100, [1, 2, 3], [1, 2, 3])
    # 5 全能量进位
    write_file(5, 10, [6, 7, 8], [5, 6, 4])
    # 6 全 0
    write_file(6, 9, [0, 0, 0, 0], [0, 0, 0, 0])
    # 7 随机小，hack 只按大小对位不看进位
    q = 20
    x = [rng.randint(0, q - 1) for _ in range(15)]
    y = [rng.randint(0, q - 1) for _ in range(15)]
    write_file(7, q, x, y)
    # 8 一半贴着模数、一半很小
    q = 1000
    x = [rng.randint(0, 10) for _ in range(20)] + [rng.randint(q - 20, q - 1) for _ in range(20)]
    y = [rng.randint(0, 10) for _ in range(20)] + [rng.randint(q - 20, q - 1) for _ in range(20)]
    write_file(8, q, x, y)
    # 9 中等
    k, q = 80000, 10 ** 9
    x = [rng.randint(0, q - 1) for _ in range(k)]
    y = [rng.randint(0, q - 1) for _ in range(k)]
    write_file(9, q, x, y)
    # 10 上限
    k, q = 300000, 10 ** 9
    x = [rng.randint(0, q - 1) for _ in range(k)]
    y = [rng.randint(0, q - 1) for _ in range(k)]
    write_file(10, q, x, y)


if __name__ == "__main__":
    main()
