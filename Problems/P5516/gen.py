# -*- coding: utf-8 -*-
"""P5516 生成 10 组数据并用 std.py 重算校验。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551620260922)


def solve(a):
    n = len(a)
    left = [1] * n
    right = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and left[j] + 1 > left[i]:
                left[i] = left[j] + 1
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if a[j] < a[i] and right[j] + 1 > right[i]:
                right[i] = right[j] + 1
    ans = 0
    for i in range(n):
        if left[i] >= 2 and right[i] >= 2:
            ans = max(ans, left[i] + right[i] - 1)
    return ans


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
        [2, 1, 4, 7, 3, 2, 5, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [1, 3, 2],
        [1, 2, 2, 1],
        [1, 5, 1, 5, 1],
        [RNG.randint(1, 100) for _ in range(30)],
        list(range(1, 101)) + list(range(99, 0, -1)),
        [RNG.randint(1, 10**9) for _ in range(5000)],
        [RNG.randint(1, 10**9) for _ in range(5000)],
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
    print("P5516 gen ok")


if __name__ == "__main__":
    main()
