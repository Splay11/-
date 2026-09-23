# -*- coding: utf-8 -*-
"""P5315 造数：单调栈求独占亮源。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(p, s, r):
    left = [-1] * p
    st = []
    for i in range(p):
        while st and r[st[-1]] < r[i]:
            st.pop()
        if st:
            left[i] = st[-1]
        st.append(i)
    right = [p] * p
    st = []
    for i in range(p - 1, -1, -1):
        while st and r[st[-1]] < r[i]:
            st.pop()
        if st:
            right[i] = st[-1]
        st.append(i)
    peaks = []
    for i in range(p):
        ok_l = left[i] < 0 or i - left[i] > s
        ok_r = right[i] >= p or right[i] - i > s
        if ok_l and ok_r:
            peaks.append(i + 1)
    return peaks


def write_file(idx, p, s, r):
    assert 1 <= p <= 200000
    assert 0 <= s <= 200000
    assert len(r) == p
    for x in r:
        assert -10 ** 9 <= x <= 10 ** 9
    lines = ["%d %d" % (p, s), " ".join(str(x) for x in r)]
    peaks = solve(p, s, r)
    out = str(len(peaks)) + "\n" + " ".join(str(x) for x in peaks)
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def main():
    rng = random.Random(53151)

    write_file(1, 6, 2, [2, 8, 1, 5, 9, 3])
    write_file(2, 4, 0, [1, 1, 1, 1])
    write_file(3, 3, 1, [5, 5, 4])
    # 4 严格递增，半径 1 时只有最右
    write_file(4, 5, 1, [1, 2, 3, 4, 5])
    # 5 严格递减，半径 1 时只有最左
    write_file(5, 5, 1, [9, 7, 5, 3, 1])
    # 6 半径大于长度，只有全局唯一最大
    write_file(6, 6, 100, [1, 4, 2, 9, 3, 8])
    # 7 含负数与重复
    write_file(7, 7, 2, [-3, -3, 0, -1, 0, 5, 5])
    # 8 随机中等
    p = 50
    write_file(8, p, rng.randint(0, 20), [rng.randint(-1000, 1000) for _ in range(p)])
    # 9 大数据
    p = 180000
    write_file(9, p, 3, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(p)])
    # 10 最大规模，s=0 全部入选
    p = 200000
    write_file(10, p, 0, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(p)])


if __name__ == "__main__":
    main()
