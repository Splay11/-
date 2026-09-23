# -*- coding: utf-8 -*-
"""P5514 生成 10 组数据并用 std.py 重算校验。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551420260922)
INF = 10**30


def solve(a):
    f = a[0]
    g = INF
    for i in range(1, len(a)):
        ng = min(f, g)
        nf = a[i] + (0 if g >= INF // 2 else min(0, g))
        f, g = nf, ng
    return min(f, g)


def write_in(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def main():
    DATA.mkdir(exist_ok=True)
    cases = [
        [3, -2, 5, -1, -4],
        [2, -5, 3],
        [7],
        [1, 2, 3, 4, 5],
        [-1, -2, -3, -4],
        [5, -1, -100, -1, 5],
        [0, 0, 0],
        [RNG.randint(-100, 100) for _ in range(20)],
        [RNG.randint(-(10**9), 10**9) for _ in range(10**5)],
        [RNG.randint(-(10**9), 10**9) for _ in range(10**5)],
    ]
    for i, a in enumerate(cases, 1):
        write_in(DATA / f"{i}.in", f"{len(a)}\n" + " ".join(map(str, a)))
        write_out(DATA / f"{i}.out", solve(a))

    for i in range(1, 11):
        inp = (DATA / f"{i}.in").read_bytes()
        r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=inp, capture_output=True)
        assert r.returncode == 0, r.stderr.decode()
        got = r.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert got == (DATA / f"{i}.out").read_bytes(), i
    print("P5514 gen ok")


if __name__ == "__main__":
    main()
