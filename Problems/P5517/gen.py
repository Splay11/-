# -*- coding: utf-8 -*-
"""P5517 生成 10 组数据并用 std.py 重算校验。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(551720260922)


def kadane(a):
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def solve(a, k):
    one = kadane(a)
    if k == 1:
        return one
    total = sum(a)
    s = 0
    max_pref = a[0]
    for x in a:
        s += x
        max_pref = max(max_pref, s)
    s = 0
    max_suf = a[-1]
    for x in reversed(a):
        s += x
        max_suf = max(max_suf, s)
    ans = max(one, max_suf + max_pref)
    if k > 2 and total > 0:
        ans = max(ans, max_suf + (k - 2) * total + max_pref)
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
        (1, [1, -2, 3]),
        (3, [1, 2, -1, 3]),
        (5, [-1, -2, -3]),
        (4, [5]),
        (3, [1, -2]),
        (10, [2, -1, 2]),
        (2, [RNG.randint(-50, 50) for _ in range(15)]),
        (5, [RNG.randint(-100, 100) for _ in range(50)]),
        (10000, [RNG.randint(-(10**9), 10**9) for _ in range(10**5)]),
        (10**4, [RNG.randint(-(10**6), 10**6) for _ in range(10**5)]),
    ]
    for i, (k, a) in enumerate(cases, 1):
        write_in(DATA / f"{i}.in", f"{len(a)} {k}\n" + " ".join(map(str, a)))
        write_out(DATA / f"{i}.out", solve(a, k))

    for i in range(1, 11):
        inp = (DATA / f"{i}.in").read_bytes()
        r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=inp, capture_output=True)
        assert r.returncode == 0, r.stderr.decode()
        got = r.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert got == (DATA / f"{i}.out").read_bytes(), i
    print("P5517 gen ok")


if __name__ == "__main__":
    main()
