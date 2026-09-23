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


def make_case(arr):
    return "%d\n%s" % (len(arr), " ".join(str(x) for x in arr))


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5502)
    cases = [
        "3\n8 -8 -2",
        "2\n-8 -8",
        make_case([1]),
        make_case([1, 2, 3, 4, 5]),
        make_case([5, 4, 3, 2, 1]),
        make_case([1, 3, 2, 4]),
        make_case([0, 0, 0]),
        make_case([-5, -1, 0, 2, 10]),
        # 接近上限
        make_case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)]),
        make_case(list(range(1, 100001))),
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
            raise AssertionError("recheck fail %d got=%r exp=%r" % (i, got, exp))
    print("all ok")


if __name__ == "__main__":
    main()
