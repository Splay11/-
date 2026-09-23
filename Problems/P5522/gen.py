# -*- coding: utf-8 -*-
"""P5522 异或和为 k 的子数组个数."""
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


def dump(n, k, a):
    return "%d %d\n%s" % (n, k, " ".join(map(str, a)))


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
    rng = random.Random(5522)
    cases = [
        dump(5, 6, [8, 0, 6, 7, 3]),          # 样例1
        dump(1, 0, [0]),                      # 单元素，k=0
        dump(1, 5, [5]),                      # 单元素等于 k
        dump(4, 0, [1, 1, 1, 1]),             # 异或成对
        dump(3, 7, [7, 0, 7]),                # 含 0
        dump(6, 1, [1, 2, 3, 4, 5, 6]),
        dump(5, 0, [0, 0, 0, 0, 0]),          # 全 0，k=0
        dump(8, 3, [rng.randint(0, 15) for _ in range(8)]),
        dump(NMAX, 0, [rng.randint(0, 10 ** 9) for _ in range(NMAX)]),
        dump(NMAX, rng.randint(0, 10 ** 9),
             [rng.randint(0, 10 ** 9) for _ in range(NMAX)]),
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("case", i, "ok")


if __name__ == "__main__":
    main()
