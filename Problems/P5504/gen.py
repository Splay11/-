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


def make_case(n, m, k, mat):
    lines = ["%d %d %d" % (n, m, k)]
    for row in mat:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines)


def rand_mat(rng, n, m):
    return [[rng.randint(-10 ** 9, 10 ** 9) for _ in range(m)] for _ in range(n)]


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5504)
    sample1 = (
        "5 4 1\n"
        "25 -39 100 39\n"
        "-91 63 23 -26\n"
        "-28 60 46 -32\n"
        "-5 2 27 -1\n"
        "-92 66 -23 54"
    )
    sample2 = (
        "4 4 2\n"
        "87 -57 38 4\n"
        "-53 -75 -46 -77\n"
        "71 -43 49 76\n"
        "-30 6 -75 96"
    )
    cases = [
        sample1,
        sample2,
        make_case(1, 1, 1, [[7]]),
        make_case(3, 3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        make_case(2, 5, 2, [[1, -1, 2, -2, 3], [0, 0, 0, 0, 0]]),
        make_case(4, 2, 1, [[-5, 5], [1, 1], [2, -2], [0, 9]]),
        make_case(5, 5, 3, rand_mat(rng, 5, 5)),
        make_case(10, 10, 5, rand_mat(rng, 10, 10)),
        # 较大数据。1000×1000 时 Java 在 256MB 下会 MLE，收到 160。
        make_case(160, 160, 1, rand_mat(rng, 160, 160)),
        make_case(160, 160, 80, rand_mat(rng, 160, 160)),
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
