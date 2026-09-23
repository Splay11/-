# -*- coding: utf-8 -*-
"""P5495：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import max_candies  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(549520260921)


def brute(candies: list[int], k: int) -> int:
    mx = max(candies)
    ans = 0
    for v in range(1, mx + 1):
        got = 0
        for c in candies:
            got += c // v
        if got >= k:
            ans = v
    return ans


def write_in(path: Path, candies: list[int], k: int) -> None:
    lines = [str(len(candies)) + " " + str(k), " ".join(str(x) for x in candies)]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def dump_case(idx: int, candies: list[int], k: int, check_brute: bool = False) -> None:
    ans = max_candies(candies, k)
    if check_brute:
        b = brute(candies, k)
        if ans != b:
            raise SystemExit(f"brute mismatch {idx}: {ans} vs {b}")
    write_in(DATA / f"{idx}.in", candies, k)
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
    text = """# P5495 测例说明

输入两行：$n$ 与 $k$，然后 $n$ 堆糖果。输出每人最多颗数。`.in` 无末尾换行，`.out` 恰好一个换行。

- 1～2：原题两个样例。
- 3：$k=1$，答案是最大堆。
- 4：全相等。
- 5：总糖少于 $k$，答案 $0$。
- 6：刚好能按 $1$ 颗分完。
- 7：小随机，与线性枚举对拍。
- 8：卡「把所有堆加起来均分」（不允许合并）。
- 9：$n=10^{5}$ 随机。
- 10：$n=10^{5}$ 全是 $1$，$k=10^{12}$，答案 $0$，卡 `int` 存 $k$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [5, 8, 6], 3, True)
    dump_case(2, [2, 5], 11, True)
    dump_case(3, [4, 9, 2], 1, True)
    dump_case(4, [7, 7, 7, 7], 4, True)
    dump_case(5, [1, 1, 1], 10, True)
    dump_case(6, [3, 3, 3], 9, True)
    dump_case(7, [RNG.randint(1, 30) for _ in range(8)], RNG.randint(1, 20), True)
    dump_case(8, [10, 1, 1], 3, True)
    n = 10**5
    dump_case(9, [RNG.randint(1, 10**7) for _ in range(n)], RNG.randint(1, 10**6))
    dump_case(10, [1] * n, 10**12)
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
