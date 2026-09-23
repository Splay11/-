# -*- coding: utf-8 -*-
import os
import random
import subprocess
import sys
import string

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


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(5501)
    letters = string.ascii_lowercase
    cases = [
        "js",
        "cpgaaiczahcrtbxambcbc",
        "b",
        "ac",
        "aac",
        "aacc",
        "bacb",
        "ababcbac",
        # 接近上限
        "".join(rng.choice(letters) for _ in range(100000)),
        "a" * 50000 + "c" * 50000,
    ]
    for i, inp in enumerate(cases, 1):
        write_in(os.path.join(DATA, "%d.in" % i), inp)
        out = run_std(inp)
        write_out(os.path.join(DATA, "%d.out" % i), out)
        print("wrote", i, "len", len(inp))
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
