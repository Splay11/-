# -*- coding: utf-8 -*-
"""P5319 造数：明暗交错子序列按长度再字典序取第 q 条。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)

INF = 10 ** 18 + 5


def add(a, b):
    s = a + b
    return INF if s > INF else s


def solve(m, q, b):
    ways0 = [0] * (m + 1)
    ways1 = [0] * (m + 1)
    pre0 = [0] * (m + 1)
    pre1 = [0] * (m + 1)
    for i in range(m):
        cur = [0] * (m + 1)
        cur[1] = 1
        if b[i] == "0":
            for L in range(2, i + 2):
                cur[L] = pre1[L - 1]
        else:
            for L in range(2, i + 2):
                cur[L] = pre0[L - 1]
        for L in range(1, i + 2):
            start = b[i] if L % 2 == 1 else ("1" if b[i] == "0" else "0")
            if start == "0":
                ways0[L] = add(ways0[L], cur[L])
            else:
                ways1[L] = add(ways1[L], cur[L])
        if b[i] == "0":
            for L in range(1, i + 2):
                pre0[L] = add(pre0[L], cur[L])
        else:
            for L in range(1, i + 2):
                pre1[L] = add(pre1[L], cur[L])
    q -= 1
    for L in range(1, m + 1):
        for start, cnt in ((0, ways0[L]), (1, ways1[L])):
            if q <= cnt:
                t = []
                bit = start
                for _ in range(L):
                    t.append(str(bit))
                    bit = 1 - bit
                return "".join(t)
            q -= cnt
    return "-1"


def write_file(idx, m, q, b):
    assert 1 <= m <= 2000
    assert 2 <= q <= 10 ** 15
    assert len(b) == m and set(b) <= set("01")
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("%d %d\n%s" % (m, q, b))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(solve(m, q, b) + "\n")


def main():
    rng = random.Random(5319)
    write_file(1, 3, 4, "110")
    write_file(2, 4, 2, "0101")
    write_file(3, 1, 5, "0")
    # 4 全 1，只有空串和 n 条 "1"
    write_file(4, 5, 3, "11111")
    # 5 不存在
    write_file(5, 2, 100, "00")
    # 6 hack：长度优先，不是标准字典序（01 应排在 1 后面）
    write_file(6, 2, 3, "01")
    # 7 交错最长
    write_file(7, 6, 8, "010101")
    # 8 随机中等
    m = 40
    write_file(8, m, rng.randint(2, 80), "".join(rng.choice("01") for _ in range(m)))
    # 9 较大
    m = 800
    write_file(9, m, 10 ** 9, "".join(rng.choice("01") for _ in range(m)))
    # 10 上限，大名次
    m = 2000
    write_file(10, m, 10 ** 15, "".join(rng.choice("01") for _ in range(m)))


if __name__ == "__main__":
    main()
