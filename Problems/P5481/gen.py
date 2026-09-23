# -*- coding: utf-8 -*-
"""P5481 数组变为非正：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_ops  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(548120260920)


def write_in(path: Path, heavy: int, light: int, load: list[int]) -> None:
    lines = [str(len(load)), f"{heavy} {light}", " ".join(str(x) for x in load)]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def dump(idx: int, heavy: int, light: int, load: list[int]) -> None:
    write_in(DATA / f"{idx}.in", heavy, light, load)
    write_out(DATA / f"{idx}.out", min_ops(load, heavy, light))


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
    text = """# P5481 测例说明

输入三行：$n$，然后 $A\\ B$，然后 $n$ 个 $a_i$。输出最少次数。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：样例 1。两次第二种操作打在两个 $3$ 上，答案 $2$。
- 2：样例 2。$n=1$，只能减 $A$。
- 3：先减 $A$ 造出发射点，再对其余减 $B$。
- 4：卡「两种效果写成同一次操作」的假解，XOR 答案大于同时减。
- 5：全体相等，第二种操作摊开优于全减 $A$。
- 6：$A=B+1$，差额极小。
- 7：随机小数据。
- 8：$n=80$，中等。
- 9：$n=200$，$B=1$ 压测枚举 $S$。
- 10：$n=200$，$a_i$ 拉到 $10^5$。

hack 点：把一次操作写成同时减 $A$ 和其余减 $B$、第二种操作总打在同一个下标、忘记 $n=1$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    dump(1, 6, 4, [3, 7, 3])
    dump(2, 7, 2, [20])
    dump(3, 7, 2, [2, 9, 6])
    dump(4, 5, 2, [10, 8, 3, 6, 4])
    dump(5, 4, 2, [8, 8, 8, 8])
    dump(6, 3, 2, [9, 6, 5, 4, 1])
    dump(7, 9, 4, [RNG.randint(1, 50) for _ in range(8)])
    dump(8, 100, 7, [RNG.randint(1, 1000) for _ in range(80)])
    dump(9, 2, 1, [RNG.randint(1, 1000) for _ in range(200)])
    dump(10, 100000, 1, [10**5] * 200)

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
