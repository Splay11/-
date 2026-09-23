# -*- coding: utf-8 -*-
"""P5308 造数：网格只右/下，边权为灰尘差绝对值的最短路 DP。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(d):
    r = len(d)
    c = len(d[0])
    dp = [[0] * c for _ in range(r)]
    for j in range(1, c):
        dp[0][j] = dp[0][j - 1] + abs(d[0][j] - d[0][j - 1])
    for i in range(1, r):
        dp[i][0] = dp[i - 1][0] + abs(d[i][0] - d[i - 1][0])
    for i in range(1, r):
        for j in range(1, c):
            up = dp[i - 1][j] + abs(d[i][j] - d[i - 1][j])
            left = dp[i][j - 1] + abs(d[i][j] - d[i][j - 1])
            dp[i][j] = min(up, left)
    return dp[r - 1][c - 1]


def write_case(idx, d):
    r = len(d)
    c = len(d[0])
    assert 1 <= r <= 200 and 1 <= c <= 200
    for i in range(r):
        assert len(d[i]) == c
        for j in range(c):
            assert 0 <= d[i][j] <= 10000
    ans = solve(d)
    lines = ["%d %d" % (r, c)]
    for i in range(r):
        lines.append(" ".join(str(x) for x in d[i]))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")


def rnd_grid(rng, r, c, lo, hi):
    return [[rng.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def main():
    rng = random.Random(5308)

    # 1 改写样例1
    write_case(1, [[2, 2, 5, 1]])
    # 2 改写样例2
    write_case(2, [[0, 5], [1, 2], [4, 3]])
    # 3 单格
    write_case(3, [[9]])
    # 4 单列
    write_case(4, [[3], [10], [4], [4], [0]])
    # 5 全零
    write_case(5, [[0, 0, 0], [0, 0, 0]])
    # 6 卡逐步贪心（每步选差值更小的方向）
    write_case(6, [[0, 10, 11], [1, 100, 12]])
    # 7 极值灰尘
    write_case(7, [[0, 10000], [10000, 0], [1, 9999]])
    # 8 中等随机
    write_case(8, rnd_grid(rng, 12, 15, 0, 200))
    # 9 满规模随机
    write_case(9, rnd_grid(rng, 200, 200, 0, 10000))
    # 10 满规模高低交错，压路径选择
    g = []
    for i in range(200):
        row = []
        for j in range(200):
            row.append(10000 if (i + j) % 2 == 0 else 0)
        g.append(row)
    write_case(10, g)

    for i in range(1, 11):
        with open(os.path.join(DIR, "%d.in" % i), "r", encoding="utf-8") as f:
            raw = f.read()
        assert not raw.endswith("\n"), "输入末尾多了换行: %d.in" % i
        lines = raw.split("\n")
        r, c = map(int, lines[0].split())
        d = []
        for k in range(1, r + 1):
            d.append(list(map(int, lines[k].split())))
        with open(os.path.join(DIR, "%d.out" % i), "r", encoding="utf-8") as f:
            out = f.read()
        assert out.endswith("\n") and out.count("\n") == 1
        got = solve(d)
        exp = int(out.strip())
        assert got == exp, "对拍失败 %d: %s vs %s" % (i, got, exp)
    print("ok")


if __name__ == "__main__":
    main()
