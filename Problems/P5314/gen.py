# -*- coding: utf-8 -*-
"""P5314 造数：渗水量降序，前 u 处封堵、接着 v 处引流。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(k, u, v, g, h):
    h = sorted(h, reverse=True)
    ans = 0
    for i in range(k):
        if i < u:
            continue
        if i < u + v:
            val = h[i] - g
            if val < 0:
                val = 0
            ans += val
        else:
            ans += h[i]
    return ans


def write_file(idx, k, u, v, g, h):
    assert 1 <= k <= 200000
    assert 0 <= u <= k and 0 <= v <= k
    assert 1 <= g <= 10 ** 9
    assert len(h) == k
    for x in h:
        assert 0 <= x <= 10 ** 9
    lines = ["%d %d %d %d" % (k, u, v, g), " ".join(str(x) for x in h)]
    out = str(solve(k, u, v, g, h))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def main():
    rng = random.Random(53141)

    # 1 改写样例1
    write_file(1, 4, 1, 1, 5, [12, 3, 9, 1])
    # 2 样例2：只有引流
    write_file(2, 3, 0, 2, 10, [4, 25, 6])
    # 3 样例3：单点 0
    write_file(3, 1, 0, 0, 1, [0])
    # 4 令牌足够覆盖全部
    write_file(4, 3, 2, 2, 10, [5, 6, 7])
    # 5 卡 int：大渗水量累加
    write_file(5, 3, 1, 0, 1, [10 ** 9, 10 ** 9, 10 ** 9])
    # 6 hack：封堵应给最大，若先引流最大会多残留
    write_file(6, 2, 1, 1, 5, [10, 3])
    # 7 引流把小值打成 0
    write_file(7, 4, 0, 2, 100, [50, 200, 3, 100])
    # 8 随机中等
    k = 40
    write_file(
        8,
        k,
        rng.randint(0, k),
        rng.randint(0, k),
        rng.randint(1, 10 ** 6),
        [rng.randint(0, 10 ** 6) for _ in range(k)],
    )
    # 9 大数据接近上限
    k = 180000
    write_file(
        9,
        k,
        k // 3,
        k // 4,
        10 ** 9,
        [rng.randint(0, 10 ** 9) for _ in range(k)],
    )
    # 10 最大规模 + 全暂缓，卡 64 位
    k = 200000
    write_file(10, k, 0, 0, 1, [10 ** 9] * k)


if __name__ == "__main__":
    main()
