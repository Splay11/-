# -*- coding: utf-8 -*-
"""P5328 造数：栈出入库唯一序列。"""
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(k, v):
    st = []
    ops = []
    need = 1
    for x in v:
        st.append(x)
        ops.append("I")
        while st and st[-1] == need:
            st.pop()
            ops.append("O")
            need += 1
    if need == k + 1:
        return "".join(ops)
    return "N"


def write_file(idx, k, v):
    assert 1 <= k <= 200000
    assert sorted(v) == list(range(1, k + 1))
    lines = [str(k), " ".join(str(x) for x in v)]
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(solve(k, v) + "\n")


def main():
    rng = random.Random(5328)
    write_file(1, 4, [3, 1, 2, 4])
    write_file(2, 3, [2, 3, 1])
    write_file(3, 1, [1])
    write_file(4, 3, [1, 2, 3])
    write_file(5, 3, [3, 2, 1])
    # 6 递减到一半再乱序，常见不可行
    write_file(6, 5, [2, 3, 5, 4, 1])
    write_file(7, 8, list(range(1, 9)))
    p = list(range(1, 41))
    rng.shuffle(p)
    write_file(8, 40, p)
    p = list(range(1, 80001))
    rng.shuffle(p)
    write_file(9, 80000, p)
    write_file(10, 200000, list(range(200000, 0, -1)))


if __name__ == "__main__":
    main()
