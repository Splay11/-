# -*- coding: utf-8 -*-
"""P5520 分割使方差和最大."""
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


def dump(n, a):
    return "%d\n%s" % (n, " ".join(map(str, a)))


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
    rng = random.Random(5520)
    cases = [
        dump(3, [-1, 9, -9]),                 # 样例1
        dump(4, [2, 1, 7, 2]),                # 样例2
        dump(2, [0, 0]),                      # 最小 n
        dump(2, [-10 ** 6, 10 ** 6]),         # 极值两端
        dump(5, [1, 1, 1, 1, 1]),             # 全相同
        dump(6, [1, 2, 3, 4, 5, 6]),          # 递增
        dump(7, [9, -9, 9, -9, 9, -9, 9]),    # 交替
        dump(10, [rng.randint(-100, 100) for _ in range(10)]),
        # 值域收窄，避免超大方差在 %.6f 上三语言舍入不一致
        dump(NMAX, [rng.randint(-1000, 1000) for _ in range(NMAX)]),
        dump(NMAX, [rng.randint(-500, 500) for _ in range(NMAX)]),
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok")


if __name__ == "__main__":
    main()
