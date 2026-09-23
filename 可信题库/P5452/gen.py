# -*- coding: utf-8 -*-
"""P5452 造数：围桌凉菜合并。"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5452)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return "[" + ", ".join(str(x) for x in a) + "]"


def solve(a: List[int]) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution().minCircleMerge(a)


def write_case(idx: int, arr: List[int]) -> None:
    assert 2 <= len(arr) <= 400
    assert all(1 <= x <= 100 for x in arr)
    ans = solve(arr)
    (DATA / f"{idx}.in").write_text(fmt_arr(arr) + "\n", encoding="utf-8")
    (DATA / f"{idx}.out").write_text(str(ans) + "\n", encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []
    # 1-3 样例
    cases.append([1, 1, 1])
    cases.append([1, 2, 3, 4])
    cases.append([10, 20])
    # 4 全相等
    cases.append([5] * 8)
    # 5 递增
    cases.append(list(range(1, 21)))
    # 6 递减
    cases.append(list(range(30, 0, -1)))
    # 7 小随机
    cases.append([RNG.randint(1, 100) for _ in range(15)])
    # 8 中等
    cases.append([RNG.randint(1, 100) for _ in range(80)])
    # 9 边界大：n=400
    cases.append([RNG.randint(1, 100) for _ in range(400)])
    # 10 两端大、中间小（卡贪心）
    mid = [1] * 50
    cases.append([100] + mid + [100])

    for i, arr in enumerate(cases, 1):
        write_case(i, arr)
        print(f"case {i}: n={len(arr)} ans={solve(arr)}")
    print("ok")


if __name__ == "__main__":
    main()
