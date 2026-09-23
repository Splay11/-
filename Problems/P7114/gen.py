# -*- coding: utf-8 -*-
"""P7114 造数：记忆化 DFS 满分；普通递归只过前 7 组。"""
from __future__ import annotations

from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7114)


def first_wins(n, k):
    return n % (k + 1) != 0


def who_wins(n, k):
    return "YES" if first_wins(n, k) else "NO"


def write_case(idx, n, k):
    assert 1 <= n <= 1000 and 1 <= k <= 1000
    (DATA / f"{idx}.in").write_bytes(f"{n} {k}".encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(who_wins(n, k) + "\n")
    return who_wins(n, k)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    # 1~7：n、k 都很小，无记忆化递归也能很快算完
    # 8~10：n 大约 30~40、k 较大，无记忆化会指数爆炸 TLE；
    #       n 仍远小于 1000，记忆化 DFS 递归深度和 O(nk) 都能过
    cases = [
        (10, 3),
        (4, 3),
        (1, 1),
        (7, 7),
        (9, 1),
        (RNG.randint(10, 16), RNG.randint(2, 4)),
        (6, 3),
        (32, 10),
        (36, 8),
        (40, 12),
    ]

    notes = [
        "样例 10 3，YES",
        "样例 4 3，NO",
        "n=k=1，YES",
        "n=k，一次取完，YES",
        "k=1 奇数，YES",
        "随机很小，普通递归可过",
        "hack n=6 k=3：n%k=0 但 YES",
        "n=32 k=10，卡普通递归",
        "n=36 k=8，卡普通递归",
        "n=40 k=12，卡普通递归",
    ]

    for i, (n, k) in enumerate(cases, 1):
        ans = write_case(i, n, k)
        print(f"case {i}: n={n} k={k} ans={ans} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        n, k = map(int, raw.split())
        got = who_wins(n, k)
        expect = (DATA / f"{i}.out").read_text(encoding="utf-8").strip()
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        if (DATA / f"{i}.in").read_bytes().endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    print("gen ok")


if __name__ == "__main__":
    main()
