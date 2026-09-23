# -*- coding: utf-8 -*-
"""P5515 生成 10 组数据并用 std.py 重算校验。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def solve(S):
    dp = [0] * (S + 1)
    dp[0] = 1
    for _ in range(10):
        ndp = [0] * (S + 1)
        for s in range(S + 1):
            if dp[s] == 0:
                continue
            for v in range(11):
                if s + v <= S:
                    ndp[s + v] += dp[s]
        dp = ndp
    return dp[S]


def write_in(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def main():
    DATA.mkdir(exist_ok=True)
    cases = [0, 1, 2, 5, 10, 25, 50, 75, 99, 100]
    for i, S in enumerate(cases, 1):
        write_in(DATA / f"{i}.in", str(S))
        write_out(DATA / f"{i}.out", solve(S))

    for i in range(1, 11):
        inp = (DATA / f"{i}.in").read_bytes()
        r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=inp, capture_output=True)
        assert r.returncode == 0, r.stderr.decode()
        got = r.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert got == (DATA / f"{i}.out").read_bytes(), i
    print("P5515 gen ok")


if __name__ == "__main__":
    main()
