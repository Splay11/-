# -*- coding: utf-8 -*-
"""P5355 造数：最少相邻合并使序列不降。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5355)


def load_std():
    spec = importlib.util.spec_from_file_location("p5355_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.min_ops


min_ops = load_std()


def dp_n2(a):
    n = len(a)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    inf = 10**9
    d = [inf] * (n + 1)
    last = [0] * (n + 1)
    d[0] = 0
    for i in range(1, n + 1):
        best = inf
        bl = 0
        for j in range(i):
            seg = pre[i] - pre[j]
            if last[j] <= seg:
                ops = d[j] + (i - j - 1)
                if ops < best or (ops == best and seg < bl):
                    best = ops
                    bl = seg
        d[i] = best
        last[i] = bl
    return d[n]


def write_case(idx, tests):
    q = len(tests)
    assert 1 <= q <= 25
    outs = []
    lines = [str(q)]
    for arr in tests:
        m = len(arr)
        assert 1 <= m <= 5000
        assert all(1 <= x <= 10**9 for x in arr)
        lines.append(str(m))
        lines.append(" ".join(str(x) for x in arr))
        outs.append(str(min_ops(arr)))
    (DATA / f"{idx}.in").write_bytes("\n".join(lines).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(outs) + "\n")
    return outs


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []
    cases.append([[5, 2, 6], [1, 3, 8], [4, 1, 6, 6]])
    cases.append([[9, 8, 7], [6, 3, 3, 1, 8]])
    cases.append([[12]])
    cases.append([[1, 2, 3, 4, 5]])
    cases.append([[9, 7, 5, 3, 1]])
    cases.append([[4, 1, 6, 6], [10, 1, 1, 1], [2, 2, 2]])
    cases.append([[RNG.randint(1, 30) for _ in range(8)] for _ in range(5)])
    cases.append([[RNG.randint(1, 1000) for _ in range(40)] for _ in range(10)])
    cases.append([[RNG.randint(1, 10**9) for _ in range(5000)] for _ in range(25)])
    cases.append([[5000 - i for i in range(5000)] for _ in range(25)])

    notes = [
        "样例1",
        "样例2",
        "样例3 m=1",
        "已不降",
        "严格下降",
        "卡左贪心 (4,1,6,6)",
        "短随机对拍",
        "中等随机",
        "q=25 m=5000 随机",
        "q=25 m=5000 递减",
    ]
    for i, tests in enumerate(cases, 1):
        outs = write_case(i, tests)
        print(f"case {i}: q={len(tests)} m0={len(tests[0])} first={outs[0]} note={notes[i - 1]}")

    assert min_ops([3, 1, 2, 4]) == 1
    assert min_ops([1, 2, 3, 4]) == 0
    assert min_ops([4, 2, 3, 1, 5]) == 2
    assert min_ops([4, 1, 6, 6]) == 1

    for n in range(1, 9):
        for _ in range(80):
            a = [RNG.randint(1, 12) for _ in range(n)]
            if min_ops(a) != dp_n2(a):
                raise SystemExit(f"与 n^2 不符 {a}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        if raw.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out = (DATA / f"{i}.out").read_bytes()
        if not out.endswith(b"\n") or out.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")
    print("gen ok")


if __name__ == "__main__":
    main()
