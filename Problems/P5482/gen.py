# -*- coding: utf-8 -*-
"""P5482 选花最大收益：10 组测例。"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import max_score  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(548220260920)


def brute(types: list[int], values: list[int], k: int) -> int:
    n = len(types)
    best = None
    for comb in itertools.combinations(range(n), k):
        s = 0
        ts = set()
        for i in comb:
            s += values[i]
            ts.add(types[i])
        cur = s + len(ts) * len(ts)
        if best is None or cur > best:
            best = cur
    return best


def write_in(path: Path, types: list[int], values: list[int], k: int) -> None:
    n = len(types)
    lines = [
        str(n) + " " + str(k),
        " ".join(str(x) for x in types),
        " ".join(str(x) for x in values),
    ]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def dump_case(idx: int, types: list[int], values: list[int], k: int, check_brute: bool = False) -> None:
    ans = max_score(types, values, k)
    if check_brute:
        b = brute(types, values, k)
        if ans != b:
            raise SystemExit(f"brute mismatch case {idx}: {ans} vs {b}")
    write_in(DATA / f"{idx}.in", types, values, k)
    write_out(DATA / f"{idx}.out", ans)


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 3s
memory: 512m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5482 测例说明

输入三行：$n\\ k$，类型数组，价值数组。输出一个整数。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：样例 1。跨类型更优。
- 2：样例 2。同类型两朵优于硬凑新类型。
- 3：$n=k=1$。
- 4：全部同一类型，选前 $k$ 大再加 $1$。
- 5：类型全不同，答案是前 $k$ 大之和加 $k^{2}$。
- 6：少量类型、价值和很大。卡「种类越多越好」。
- 7：小随机，与组合枚举暴力对拍。
- 8：小数据极值。混有单朵超贵与一簇中等价。
- 9：$n=10^{5}$ 随机。卡 $O(nk)$。
- 10：$n=k=10^{5}$，类型两两不同，价值全是 $10^{9}$。卡 `int`：答案 $10^{14}+10^{10}$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [1, 1, 2], [5, 3, 4], 2, True)
    dump_case(2, [1, 1, 2], [100, 99, 1], 2, True)
    dump_case(3, [7], [9], 1, True)
    dump_case(4, [3, 3, 3, 3, 3], [1, 8, 3, 8, 2], 3, True)
    dump_case(5, [1, 2, 3, 4], [4, 1, 5, 2], 3, True)
    dump_case(6, [1, 1, 1, 2], [100, 99, 98, 1], 3, True)
    dump_case(
        7,
        [RNG.randint(1, 4) for _ in range(10)],
        [RNG.randint(1, 15) for _ in range(10)],
        RNG.randint(1, 10),
        True,
    )
    dump_case(8, [1, 2, 2, 2, 3], [50, 9, 9, 9, 8], 4, True)
    n = 10**5
    dump_case(
        9,
        [RNG.randint(1, 1000) for _ in range(n)],
        [RNG.randint(1, 10**9) for _ in range(n)],
        n // 2,
    )
    dump_case(10, list(range(1, n + 1)), [10**9] * n, n)
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
