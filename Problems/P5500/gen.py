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


def make_case(m, n, a, b):
    nums1 = a + [0] * n
    lines = ["%d %d" % (m, n)]
    lines.append(" ".join(str(x) for x in nums1))
    if n > 0:
        lines.append(" ".join(str(x) for x in b))
    return "\n".join(lines)


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5500)
    cases = [
        "3 3\n1 2 3 0 0 0\n2 5 6",
        "1 0\n1",
        make_case(0, 1, [], [5]),
        make_case(2, 0, [1, 2], []),
        make_case(3, 2, [-5, -1, 0], [-3, 4]),
        make_case(4, 4, [1, 1, 1, 1], [1, 1, 1, 1]),
        make_case(5, 5, list(range(1, 6)), list(range(6, 11))),
        make_case(5, 5, list(range(6, 11)), list(range(1, 6))),
        # 接近上限
        make_case(100, 100, sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(100)),
                  sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(100))),
        make_case(0, 200, [], sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(200))),
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
