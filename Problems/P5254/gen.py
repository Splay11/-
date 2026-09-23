# -*- coding: utf-8 -*-
"""生成 P5254 data/*.in/*.out。.in 无行末多余换行；.out 恰一换行。"""

from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 3000
SEED = 525420260816
RNG = random.Random(SEED)


def solve(n: int) -> int:
    ans = 0
    for x in range(1, n + 1):
        for y in range(x, n + 1):
            z = x ^ y
            if y <= z <= n and x + y > z:
                ans += 1
    return ans


def write_pair(idx: int, n: int, ans: int) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    assert 1 <= n <= N_MAX
    tin = str(n)
    tout = f"{ans}\n"
    if tin.endswith("\n"):
        raise RuntimeError(f"case {idx}: .in ends with newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"case {idx}: bad .out newline")
    if solve(n) != ans:
        raise RuntimeError(f"case {idx}: self-check {solve(n)} != {ans}")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))


def main() -> None:
    n8 = RNG.randint(80, 200)
    cases = [
        4,  # 1 样例：答案 0，卡把 (1,2,3) 当合法
        12,  # 2 样例：5 个合法三元组
        6,  # 3 基础：第一个非零答案 (3,5,6)
        1,  # 4 边界：最小 n
        5,  # 5 边界：仍为 0，卡「n>=3 就有解」
        3,  # 6 hack：漏三角形会把 (1,2,3) 计为 1
        10,  # 7 hack：只找到 (3,5,6) 会漏 (3,9,10)
        n8,  # 8 随机中等
        2500,  # 9 压力：原题上限附近
        3000,  # 10 压力：改写后上限
    ]
    assert len(cases) == 10
    for i, n in enumerate(cases, 1):
        ans = solve(n)
        write_pair(i, n, ans)
        print(f"{i}.in n={n} ans={ans}")


if __name__ == "__main__":
    main()
