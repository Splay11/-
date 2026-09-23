# -*- coding: utf-8 -*-
"""P5325 造数：禁止四连同色的 26 色灯带方案数。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)

MOD = 1000000007
MAXK = 200000


def precompute():
    f1 = [0] * (MAXK + 1)
    f2 = [0] * (MAXK + 1)
    f3 = [0] * (MAXK + 1)
    tot = [0] * (MAXK + 1)
    f1[1] = 26
    tot[1] = 26
    for i in range(2, MAXK + 1):
        f1[i] = tot[i - 1] * 25 % MOD
        f2[i] = f1[i - 1]
        f3[i] = f2[i - 1]
        tot[i] = (f1[i] + f2[i] + f3[i]) % MOD
    return tot


def write_file(idx, ks):
    q = len(ks)
    assert 1 <= q <= 200000
    for k in ks:
        assert 1 <= k <= 200000
    tot = write_file.tot
    lines = [str(q)] + [str(k) for k in ks]
    outs = [str(tot[k]) for k in ks]
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")


def main():
    rng = random.Random(5325)
    write_file.tot = precompute()

    # 1 改写样例1
    write_file(1, [1, 3, 5])
    # 2 改写样例2
    write_file(2, [6])
    # 3 基础：长度 4，卡「全部 26^k」
    write_file(3, [4])
    # 4 连续小值
    write_file(4, [1, 2, 3, 4, 5, 6, 7])
    # 5 hack：长度大于 4，卡只减 26 种全同色
    write_file(5, [8, 10])
    # 6 hack：禁止三连的错误 DP 会在这里偏掉
    write_file(6, [9])
    # 7 随机中等
    write_file(7, [rng.randint(1, 200) for _ in range(20)])
    # 8 若干中等询问
    write_file(8, [rng.randint(1, 5000) for _ in range(80)])
    # 9 大数据：很多询问
    write_file(9, [rng.randint(1, 200000) for _ in range(100000)])
    # 10 最大询问数，混入上限长度，卡逐询问 O(k)
    ks = [200000] * 50 + [rng.randint(1, 200000) for _ in range(199950)]
    write_file(10, ks)


if __name__ == "__main__":
    main()
