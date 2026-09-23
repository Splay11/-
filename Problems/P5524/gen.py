# -*- coding: utf-8 -*-
"""P5524 排列恢复升序的最小交换次数."""
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
NMAX = 10 ** 5


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def dump(n, p):
    return "%d\n%s" % (n, " ".join(map(str, p)))


def run_std(inp):
    p = subprocess.run(
        [sys.executable, os.path.join(DIR, "std.py")],
        input=inp, capture_output=True, text=True, encoding="utf-8"
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5524)
    rev = list(range(NMAX, 0, -1))
    randp = list(range(1, NMAX + 1))
    rng.shuffle(randp)

    cases = [
        dump(3, [2, 3, 1]),                   # 样例1
        dump(4, [1, 2, 3, 4]),                # 样例2
        dump(1, [1]),                         # 最小
        dump(2, [2, 1]),                      # 一个交换
        dump(5, [2, 1, 4, 5, 3]),             # 多环
        dump(6, [6, 5, 4, 3, 2, 1]),          # 逆序
        dump(7, [1, 2, 3, 4, 5, 6, 7]),       # 已排序
        dump(8, [2, 3, 4, 5, 6, 7, 8, 1]),    # 单大环
        dump(NMAX, rev),                      # 上限逆序
        dump(NMAX, randp),                    # 上限随机
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok")


if __name__ == "__main__":
    main()
