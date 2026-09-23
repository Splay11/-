# -*- coding: utf-8 -*-
"""P5513 生成 10 组数据并用 std.py 重算校验。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551320260922)


def solve(n, W, items):
    dp = [0] * (W + 1)
    for w, v in items:
        for j in range(W, w - 1, -1):
            nv = dp[j - w] + v
            if nv > dp[j]:
                dp[j] = nv
    return dp[W]


def write_in(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def main():
    DATA.mkdir(exist_ok=True)
    cases = []
    cases.append((3, 5, [(2, 6), (3, 8), (4, 7)]))
    cases.append((4, 5, [(1, 2), (3, 5), (2, 4), (4, 6)]))
    cases.append((1, 10, [(7, 100)]))
    cases.append((3, 3, [(2, 5), (3, 9), (1, 2)]))
    cases.append((2, 10, [(3, 4), (5, 6)]))
    n, W = 8, 20
    cases.append((n, W, [(RNG.randint(1, W), RNG.randint(1, 1000)) for _ in range(n)]))
    cases.append((5, 15, [(10, 1), (10, 100), (5, 50), (5, 50), (1, 1)]))
    n, W = 100, 500
    cases.append((n, W, [(RNG.randint(1, W), RNG.randint(1, 10**6)) for _ in range(n)]))
    for _ in range(2):
        n, W = 1000, 10000
        cases.append((n, W, [(RNG.randint(1, W), RNG.randint(1, 10**6)) for _ in range(n)]))

    for i, (n, W, items) in enumerate(cases, 1):
        lines = [f"{n} {W}"] + [f"{w} {v}" for w, v in items]
        write_in(DATA / f"{i}.in", "\n".join(lines))
        write_out(DATA / f"{i}.out", solve(n, W, items))

    # 用 std.py 重跑校验
    for i in range(1, 11):
        inp = (DATA / f"{i}.in").read_bytes()
        r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=inp, capture_output=True)
        assert r.returncode == 0, r.stderr.decode()
        got = r.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        exp = (DATA / f"{i}.out").read_bytes()
        assert got == exp, (i, got, exp)
    print("P5513 gen ok")


if __name__ == "__main__":
    main()
