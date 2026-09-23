# -*- coding: utf-8 -*-
"""P5343 造数：sum (i XOR i+1) mod 1e9+7。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5343)
MOD = 1000000007


def load_std():
    spec = importlib.util.spec_from_file_location("p5343_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.path_sum


path_sum = load_std()


def brute(n):
    s = 0
    for i in range(1, n):
        s += i ^ (i + 1)
    return s % MOD


def write_case(idx, ps):
    q = len(ps)
    assert 1 <= q <= 200000
    for p in ps:
        assert 1 <= p <= 10**18
    outs = [path_sum(p) for p in ps]
    lines = [str(q)] + [str(p) for p in ps]
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(str(x) for x in outs) + "\n")
    return outs


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    cases.append([5, 8, 7])
    cases.append([16, 4])
    cases.append([100])
    cases.append([1])
    cases.append([2, 4, 8, 16, 32, 64])
    # 卡 O(n) 暴力
    cases.append([10**18, 10**18 - 1, 2**59])
    cases.append(list(range(1, 21)))
    cases.append([RNG.randint(1, 10**6) for _ in range(40)])
    cases.append([1, 10**18] * 500)
    cases.append([RNG.choice([1, 2, 7, 10**9, 10**18]) for _ in range(100000)])

    notes = [
        "样例1",
        "样例2",
        "样例3",
        "p=1 答案 0",
        "2 的幂",
        "1e18 卡暴力",
        "1..20 与暴力对拍",
        "小随机",
        "1000 个极值交替",
        "q=1e5 压测读入",
    ]

    for i, ps in enumerate(cases, 1):
        outs = write_case(i, ps)
        print(f"case {i}: q={len(ps)} maxp={max(ps)} first={outs[0]} note={notes[i - 1]}")

    for n in range(1, 21):
        if path_sum(n) != brute(n):
            raise SystemExit(f"与暴力不符 n={n}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        q = int(lines[0])
        ps = [int(lines[j]) for j in range(1, q + 1)]
        got = [path_sum(p) for p in ps]
        expect = [int(x) for x in (DATA / f"{i}.out").read_text(encoding="utf-8").strip().split("\n")]
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    if path_sum(1) != 0:
        raise SystemExit("p=1 应为 0")
    if path_sum(10) != 35:
        raise SystemExit("原样例 n=10 公式应仍为 35")

    print("gen ok")


if __name__ == "__main__":
    main()
