# -*- coding: utf-8 -*-
"""P5326 造数：色号不降喷涂，忽略更大字母后数连续段。"""
import os
import random
import string

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(w):
    ans = 0
    for c in range(26):
        ch = chr(ord("a") + c)
        in_run = False
        for x in w:
            if x > ch:
                continue
            if x == ch:
                if not in_run:
                    ans += 1
                    in_run = True
            else:
                in_run = False
    return ans


def write_file(idx, w):
    assert 1 <= len(w) <= 100000
    assert all("a" <= ch <= "z" for ch in w)
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(w)
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(w)) + "\n")


def main():
    rng = random.Random(5326)

    write_file(1, "bab")
    write_file(2, "aabbaa")
    write_file(3, "dcba")
    # 4 单字符
    write_file(4, "z")
    # 5 全相同
    write_file(5, "kkkkkk")
    # 6 hack：成品有多段，但更大字母后喷，实际只要 2
    write_file(6, "ccaddacc")
    # 7 hack：只数不同字母会少算，被更小字母隔开的同色要多次喷
    write_file(7, "zbzbz")
    # 8 随机中等
    write_file(8, "".join(rng.choice(string.ascii_lowercase[:8]) for _ in range(80)))
    # 9 大数据随机
    write_file(9, "".join(rng.choice(string.ascii_lowercase) for _ in range(80000)))
    # 10 最大规模递减，答案等于长度
    write_file(10, "".join(chr(ord("z") - i % 26) for i in range(100000)))


if __name__ == "__main__":
    main()
