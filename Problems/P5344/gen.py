# -*- coding: utf-8 -*-
"""P5344 造数：循环硬度下最少破岩天数。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5344)


def load_std():
    spec = importlib.util.spec_from_file_location("p5344_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.min_days


min_days = load_std()


def brute(c, q, w, h):
    killed = 0
    d = 0
    while killed < q:
        d += 1
        atk = w + (d - 1) // c
        hp = h[(d - 1) % c]
        if atk >= hp:
            killed += 1
        if d > 10**7:
            raise SystemExit("brute too long")
    return d


def write_case(idx, c, q, w, h):
    assert len(h) == c
    assert 1 <= c <= 200000
    assert 1 <= q <= 10**12
    assert 0 <= w <= 10**12
    assert all(1 <= x <= 10**12 for x in h)
    ans = min_days(c, q, w, h)
    line1 = f"{c} {q} {w}"
    line2 = " ".join(str(x) for x in h)
    text_in = line1 + "\n" + line2
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    cases.append((4, 3, 2, [4, 1, 8, 3]))
    cases.append((2, 5, 0, [3, 9]))
    cases.append((1, 1, 0, [1]))
    # 初始功率已经盖过全部硬度，每天必打
    cases.append((3, 7, 100, [3, 9, 2]))
    # n=1 且需要涨功率
    cases.append((1, 5, 0, [3]))
    # 只有一个位置能打很久
    cases.append((3, 4, 0, [100, 1, 100]))
    # 功率按「每天 +1」会提早打完；正确是每 c 天才 +1
    cases.append((4, 3, 0, [10, 10, 10, 10]))
    cases.append((8, 20, 0, [RNG.randint(1, 15) for _ in range(8)]))
    # 大数据：周期拉满，q 中等
    cases.append((200000, 10**6, 0, [RNG.randint(1, 10**6) for _ in range(200000)]))
    # 满约束附近
    cases.append((200000, 10**12, 0, [10**12] * 200000))

    notes = [
        "样例1",
        "样例2",
        "样例3 p=1 要等一天",
        "w 已不小于最大硬度，答案即 q",
        "c=1 需升功率",
        "中间一天才能打",
        "卡「功率每天 +1」",
        "短周期随机",
        "c=2e5 q=1e6",
        "c=2e5 全是 1e12，卡暴力",
    ]

    for i, (c, q, w, h) in enumerate(cases, 1):
        ans = write_case(i, c, q, w, h)
        print(f"case {i}: c={c} q={q} w={w} ans={ans} note={notes[i - 1]}")

    for c, q, w, h in cases[:8]:
        b = brute(c, q, w, h)
        g = min_days(c, q, w, h)
        if b != g:
            raise SystemExit(f"与暴力不符 {h} brute={b} std={g}")

    if min_days(3, 7, 100, [3, 9, 2]) != 7:
        raise SystemExit("w 足够大时天数应等于 q")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        c, q, w = map(int, lines[0].split())
        h = list(map(int, lines[1].split()))
        got = min_days(c, q, w, h)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败 {i}")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    print("gen ok")


if __name__ == "__main__":
    main()
