# -*- coding: utf-8 -*-
"""Generate 10 test cases for P5497. First 8 small, last 2 n=q=1e5."""
from __future__ import print_function

import os
import random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def find_root(parent, delta, x):
    if parent[x] != x:
        root = find_root(parent, delta, parent[x])
        delta[x] += delta[parent[x]]
        parent[x] = root
        return root
    return x


def solve(n, k, floor_of, queries):
    parent = list(range(n + 1))
    delta = [0] * (n + 1)
    sz = [1] * (n + 1)
    invalid = 0
    for a, b, x in queries:
        if a == b:
            if x != 0:
                invalid += 1
            continue
        ra = find_root(parent, delta, a)
        rb = find_root(parent, delta, b)
        if ra == rb:
            if delta[a] - delta[b] != x:
                invalid += 1
            continue
        if floor_of[a] != floor_of[b] or sz[ra] + sz[rb] > k:
            invalid += 1
            continue
        if sz[ra] < sz[rb]:
            parent[ra] = rb
            delta[ra] = x - delta[a] + delta[b]
            sz[rb] += sz[ra]
        else:
            parent[rb] = ra
            delta[rb] = delta[a] - delta[b] - x
            sz[ra] += sz[rb]
    circles = 0
    for i in range(1, n + 1):
        if parent[i] == i:
            circles += 1
    return invalid, circles


def write_case(idx, n, q, k, floors, queries):
    assert len(floors) == n
    assert len(queries) == q
    lines = [str(n) + " " + str(q) + " " + str(k), " ".join(str(x) for x in floors)]
    for a, b, x in queries:
        lines.append(str(a) + " " + str(b) + " " + str(x))
    inp = "\n".join(lines)
    inv, cir = solve(n, k, [0] + floors, queries)
    ans = str(inv) + "\n" + str(cir) + "\n"
    with open(os.path.join(DATA, str(idx) + ".in"), "wb") as f:
        f.write(inp.encode("ascii"))
    with open(os.path.join(DATA, str(idx) + ".out"), "wb") as f:
        f.write(ans.encode("ascii"))


def main():
    os.makedirs(DATA, exist_ok=True)
    random.seed(5497)

    # 1 样例1
    write_case(1, 5, 5, 3, [1, 1, 1, 2, 2], [
        (1, 2, 5), (2, 3, 3), (1, 3, 8), (4, 5, 1), (1, 4, 2),
    ])
    # 2 样例2
    write_case(2, 4, 5, 2, [1, 1, 1, 1], [
        (1, 2, 10), (3, 4, 1), (1, 2, 9), (2, 3, 0), (1, 3, 5),
    ])
    # 3 单人，自己比自己
    write_case(3, 1, 2, 1, [7], [(1, 1, 0), (1, 1, 3)])
    # 4 K=1 无法合并
    write_case(4, 3, 3, 1, [1, 1, 1], [(1, 2, 1), (2, 3, 1), (1, 1, 0)])
    # 5 负差额传递
    write_case(5, 3, 4, 3, [5, 5, 5], [
        (1, 2, -4), (2, 3, 7), (1, 3, 3), (1, 3, 2),
    ])
    # 6 楼层不同全部作废
    write_case(6, 4, 3, 4, [1, 2, 3, 4], [(1, 2, 1), (2, 3, 1), (3, 4, 1)])
    # 7 小随机
    n7, q7, k7 = 12, 20, 5
    f7 = [random.randint(1, 3) for _ in range(n7)]
    qy7 = [(random.randint(1, n7), random.randint(1, n7), random.randint(-20, 20)) for _ in range(q7)]
    write_case(7, n7, q7, k7, f7, qy7)
    # 8 小规模链，卡 int 溢出的前奏
    n8 = 15
    f8 = [1] * n8
    qy8 = [(i, i + 1, 10 ** 9) for i in range(1, n8)]
    qy8.append((1, n8, (n8 - 1) * (10 ** 9)))
    qy8.append((1, n8, 0))
    write_case(8, n8, len(qy8), n8, f8, qy8)
    # 9 最大规模：同楼层、K 较大，随机发言
    n9 = 100000
    q9 = 100000
    k9 = 1000
    f9 = [1] * n9
    qy9 = []
    for _ in range(q9):
        a = random.randint(1, n9)
        b = random.randint(1, n9)
        x = random.randint(-10 ** 9, 10 ** 9)
        qy9.append((a, b, x))
    write_case(9, n9, q9, k9, f9, qy9)
    # 10 最大规模：多楼层 + 长链 1e9 + 超 K
    n10 = 100000
    k10 = 50
    f10 = [1 + (i % 7) for i in range(n10)]
    qy10 = []
    for i in range(1, n10):
        qy10.append((i, i + 1, 10 ** 9 if i % 2 == 0 else -(10 ** 9)))
    extra = 100000 - (n10 - 1)
    for _ in range(extra):
        a = random.randint(1, n10)
        b = random.randint(1, n10)
        qy10.append((a, b, random.randint(-10 ** 9, 10 ** 9)))
    write_case(10, n10, len(qy10), k10, f10, qy10)
    print("generated 10 cases")


if __name__ == "__main__":
    main()
