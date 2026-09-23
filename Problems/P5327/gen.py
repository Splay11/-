# -*- coding: utf-8 -*-
"""P5327 造数：最长相邻异色子串。"""
import os
import random
import string

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(w):
    best = 1
    cur = 1
    for i in range(1, len(w)):
        if w[i] != w[i - 1]:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 1
    return best


def write_file(idx, w):
    assert 1 <= len(w) < 100000
    assert all("a" <= ch <= "z" for ch in w)
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(w)
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(w)) + "\n")


def main():
    rng = random.Random(5327)
    write_file(1, "xyzzyx")
    write_file(2, "bbba")
    write_file(3, "abcab")
    write_file(4, "z")
    write_file(5, "cccccc")
    # 6 hack：整段异色中间突然断开
    write_file(6, "abcdeedcba")
    write_file(7, "".join(rng.choice("abc") for _ in range(40)))
    write_file(8, "".join(rng.choice(string.ascii_lowercase) for _ in range(200)))
    write_file(9, "".join(rng.choice(string.ascii_lowercase) for _ in range(80000)))
    # 10 接近上限，交替字母
    write_file(10, ("ab" * 49999)[:99999])


if __name__ == "__main__":
    main()
