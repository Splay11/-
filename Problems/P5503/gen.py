# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path, text):
    if not text.endswith("\n"):
        text = text + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run_std(inp):
    feed = inp if inp.endswith("\n") else inp + "\n"
    p = subprocess.run(
        [sys.executable, os.path.join(DIR, "std.py")],
        input=feed,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout if p.stdout.endswith("\n") else p.stdout + "\n"


def make_matrix(n, m, k, rows):
    lines = ["%d %d %d" % (n, m, k)]
    for row in rows:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines)


def sorted_row(rng, m, lo=1, hi=10 ** 9):
    return sorted(rng.randint(lo, hi) for _ in range(m))


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5503)
    cases = [
        "2 2 2\n246585978 285205195\n519161653 867471781",
        "3 2 6\n747831408 789078089\n230748905 878601186\n83792632 739899410",
        make_matrix(1, 1, 1, [[42]]),
        make_matrix(1, 5, 3, [[1, 2, 3, 4, 5]]),
        make_matrix(3, 1, 2, [[10], [20], [5]]),
        make_matrix(2, 3, 1, [[1, 2, 3], [4, 5, 6]]),
        make_matrix(2, 3, 6, [[1, 2, 3], [4, 5, 6]]),
        make_matrix(4, 4, 8, [sorted_row(rng, 4) for _ in range(4)]),
        # 接近上限
        make_matrix(500, 500, 1, [sorted_row(rng, 500) for _ in range(500)]),
        make_matrix(500, 500, 250000, [sorted_row(rng, 500) for _ in range(500)]),
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("wrote", i)
    for i in range(1, 11):
        with open(os.path.join(DATA, "%d.in" % i), "r", encoding="utf-8") as f:
            raw = f.read()
        got = run_std(raw)
        with open(os.path.join(DATA, "%d.out" % i), "r", encoding="utf-8") as f:
            exp = f.read()
        if got != exp:
            raise AssertionError("recheck fail %d" % i)
    print("all ok")


if __name__ == "__main__":
    main()
