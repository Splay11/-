# -*- coding: utf-8 -*-
"""P5330 造数：区间霍尔，判断每个窗能否留空。"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from std import solve

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def write_file(idx, segs):
    k = len(segs)
    assert 1 <= k <= 200000
    for p, q in segs:
        assert 1 <= p <= q <= k + 1
    lines = [str(k)]
    for p, q in segs:
        lines.append("%d %d" % (p, q))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(solve(k, segs) + "\n")


def main():
    rng = random.Random(5330)
    # 1-3 新样例
    write_file(1, [(1, 2)])
    write_file(2, [(1, 4), (2, 2), (3, 3)])
    write_file(3, [(1, 2), (1, 2), (2, 2)])
    # 4 单点只能占窗 1，hack 漏单点装满
    write_file(4, [(1, 1)])
    # 5 人人都能去任意窗，应全 1
    write_file(5, [(1, 6)] * 5)
    # 6 两个单点装满，中间不能留
    write_file(6, [(2, 2), (4, 4), (1, 5), (1, 5)])
    # 7 随机小数据
    k = 12
    segs = []
    for _ in range(k):
        p = rng.randint(1, k + 1)
        q = rng.randint(p, k + 1)
        segs.append((p, q))
    write_file(7, segs)
    # 8 局部溢出：前半挤爆，hack “只看全局多一个空窗就判全 1”
    segs = [(1, 4)] * 6
    for i in range(5, 16):
        segs.append((i, i + 2))
    write_file(8, segs)
    # 9 链式：第 i 人接受 [i,i+1]，应全 1，卡“有人区间短就乱判 0”
    k = 8000
    write_file(9, [(i, i + 1) for i in range(1, k + 1)])
    # 10 上限：少量单点装满 + 其余任意窗，答案应是单点处 0、其余 1
    k = 200000
    segs = []
    for x in range(1, 401, 5):
        segs.append((x, x))
    while len(segs) < k:
        segs.append((1, k + 1))
    write_file(10, segs)


if __name__ == "__main__":
    main()
