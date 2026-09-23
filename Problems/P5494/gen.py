# -*- coding: utf-8 -*-
"""P5494：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import smallest_divisor  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(549420260921)


def brute(nums: list[int], threshold: int) -> int:
    mx = max(nums)
    for d in range(1, mx + 1):
        s = 0
        for x in nums:
            s += (x + d - 1) // d
        if s <= threshold:
            return d
    return mx


def write_in(path: Path, nums: list[int], threshold: int) -> None:
    lines = [str(len(nums)) + " " + str(threshold), " ".join(str(x) for x in nums)]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def dump_case(idx: int, nums: list[int], threshold: int, check_brute: bool = False) -> None:
    ans = smallest_divisor(nums, threshold)
    if check_brute:
        b = brute(nums, threshold)
        if ans != b:
            raise SystemExit(f"brute mismatch {idx}: {ans} vs {b}")
    write_in(DATA / f"{idx}.in", nums, threshold)
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
    text = """# P5494 测例说明

输入两行：$n$ 与 $threshold$，然后 $n$ 个数。输出最小除数。`.in` 无末尾换行，`.out` 恰好一个换行。

- 1～3：原题三个样例。
- 4：$n=1$。
- 5：阈值等于 $n$，答案必为最大值。
- 6：全是 $1$。
- 7：小随机，与线性枚举除数对拍。
- 8：卡向下取整。
- 9：$n=5\\times 10^{4}$ 随机。
- 10：$n=5\\times 10^{4}$，全是 $10^{6}$，阈值 $=n$，答案 $10^{6}$；和可达 $5\\times 10^{10}$，卡 `int`。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [1, 2, 5, 9], 6, True)
    dump_case(2, [2, 3, 5, 7, 11], 11, True)
    dump_case(3, [19], 5, True)
    dump_case(4, [7], 7, True)
    dump_case(5, [3, 8, 2, 8], 4, True)
    dump_case(6, [1, 1, 1, 1, 1], 5, True)
    dump_case(7, [RNG.randint(1, 50) for _ in range(12)], 20, True)
    dump_case(8, [9, 9, 9], 6, True)
    n = 5 * 10**4
    dump_case(9, [RNG.randint(1, 10**6) for _ in range(n)], 10**6)
    dump_case(10, [10**6] * n, n)
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
