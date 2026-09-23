# -*- coding: utf-8 -*-
"""P5307 造数：加权曼哈顿选址（横纵加权中位数）。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def pick_median(pts):
    pts = sorted(pts, key=lambda t: t[0])
    tot = sum(w for _, w in pts)
    acc = 0
    for pos, w in pts:
        acc += w
        if acc * 2 >= tot:
            return pos
    return pts[-1][0]


def solve(a, b, w):
    P = pick_median(list(zip(a, w)))
    Q = pick_median(list(zip(b, w)))
    ans = 0
    for i in range(len(a)):
        ans += w[i] * (abs(a[i] - P) + abs(b[i] - Q))
    return ans


def write_case(idx, a, b, w):
    m = len(a)
    assert m == len(b) == len(w)
    assert 1 <= m <= 10000
    for i in range(m):
        assert -10**9 <= a[i] <= 10**9
        assert -10**9 <= b[i] <= 10**9
        assert 1 <= w[i] <= 10**6
    ans = solve(a, b, w)
    assert 0 <= ans < 2**63, "答案超出 64 位有符号范围: %s" % ans
    lines = [str(m)]
    for i in range(m):
        lines.append("%d %d %d" % (a[i], b[i], w[i]))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")


def rnd_pts(rng, m, coord, wmax):
    a = [rng.randint(-coord, coord) for _ in range(m)]
    b = [rng.randint(-coord, coord) for _ in range(m)]
    w = [rng.randint(1, wmax) for _ in range(m)]
    return a, b, w


def main():
    rng = random.Random(5307)

    # 1 改写样例1
    write_case(1, [0, 5, 5], [3, 3, 7], [2, 4, 1])
    # 2 改写样例2：最优落点不是任一居民区
    write_case(2, [0, 4, 2], [1, 1, 6], [1, 1, 1])
    # 3 单点
    write_case(3, [-8], [12], [9])
    # 4 负数坐标 + 不同权重
    write_case(4, [-20, -5, 3, 40], [7, -9, -9, 2], [3, 1, 8, 2])
    # 5 卡「不加权中位数」：左侧很多轻点，右侧一个重点
    write_case(
        5,
        [0] * 9 + [100],
        [0] * 9 + [100],
        [1] * 9 + [20],
    )
    # 6 重复坐标
    write_case(6, [2, 2, 2, 8, 8], [5, 5, 9, 5, 1], [4, 1, 1, 3, 2])
    # 7 卡 int 溢出：大坐标、中等人数
    write_case(
        7,
        [-10**9, 10**9, 0],
        [-10**9, 10**9, 10**9],
        [100000, 100000, 1],
    )
    # 8 小随机
    write_case(8, *rnd_pts(rng, 40, 1000, 50))
    # 9 满规模随机
    write_case(9, *rnd_pts(rng, 10000, 10**9, 1000))
    # 10 满规模两簇：卡「只枚举居民区当工厂」的假解仍可能碰巧，但主要压复杂度
    a = [rng.randint(-10**9, -10**9 + 50) for _ in range(5000)]
    a += [rng.randint(10**9 - 50, 10**9) for _ in range(5000)]
    b = [rng.randint(-10**9, -10**9 + 50) for _ in range(5000)]
    b += [rng.randint(10**9 - 50, 10**9) for _ in range(5000)]
    w = [rng.randint(1, 200) for _ in range(10000)]
    write_case(10, a, b, w)

    # 回读校验
    for i in range(1, 11):
        with open(os.path.join(DIR, "%d.in" % i), "r", encoding="utf-8") as f:
            raw = f.read()
        assert not raw.endswith("\n"), "输入末尾多了换行: %d.in" % i
        lines = raw.split("\n")
        m = int(lines[0])
        a, b, w = [], [], []
        for row in lines[1:]:
            ai, bi, wi = map(int, row.split())
            a.append(ai)
            b.append(bi)
            w.append(wi)
        assert len(a) == m
        with open(os.path.join(DIR, "%d.out" % i), "r", encoding="utf-8") as f:
            out = f.read()
        assert out.endswith("\n") and out.count("\n") == 1
        got = solve(a, b, w)
        exp = int(out.strip())
        assert got == exp, "对拍失败 %d: %s vs %s" % (i, got, exp)
    print("ok")


if __name__ == "__main__":
    main()
