# -*- coding: utf-8 -*-
"""P5324 造数：等待 = max(0, s_i - t)。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(k, t, s):
    ans = []
    for i in range(k):
        wait = s[i] - t
        if wait < 0:
            wait = 0
        ans.append(wait)
    return ans


def write_file(idx, k, t, s):
    assert 1 <= k <= 100000
    assert 0 <= t <= 10 ** 9
    assert len(s) == k
    assert s[-1] == 0
    for i in range(k - 1):
        assert 1 <= s[i] <= 10 ** 9
    lines = ["%d %d" % (k, t), " ".join(str(x) for x in s)]
    out = " ".join(str(x) for x in solve(k, t, s))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def main():
    rng = random.Random(5324)

    # 1 改写样例1
    write_file(1, 4, 0, [5, 3, 8, 0])
    # 2 改写样例2
    write_file(2, 4, 4, [7, 2, 10, 0])
    # 3 改写样例3：只有卸矿平台
    write_file(3, 1, 100, [0])
    # 4 基础：t 很大，全部等待为 0
    write_file(4, 5, 10 ** 9, [1, 2, 3, 4, 0])
    # 5 hack：路程不单调，卡「把后段路程求和」的假解
    write_file(5, 4, 0, [3, 10, 1, 0])
    # 6 hack：卡「改用下一个硐口路程」或漏掉 max(0,·)
    write_file(6, 5, 6, [6, 9, 1, 8, 0])
    # 7 构造：严格递减
    write_file(7, 6, 5, [20, 16, 12, 8, 3, 0])
    # 8 随机中等
    k = 40
    s = [rng.randint(1, 10 ** 6) for _ in range(k - 1)] + [0]
    write_file(8, k, rng.randint(0, 10 ** 6), s)
    # 9 大数据
    k = 80000
    s = [rng.randint(1, 10 ** 9) for _ in range(k - 1)] + [0]
    write_file(9, k, rng.randint(0, 10 ** 9), s)
    # 10 最大规模
    k = 100000
    s = [10 ** 9] * (k - 1) + [0]
    write_file(10, k, 1, s)


if __name__ == "__main__":
    main()
