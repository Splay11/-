# -*- coding: utf-8 -*-
"""P5465 待发热度重排：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import can_match  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(546520260918)


def fmt_case(p: list[int], h: list[int], t: list[int]) -> list[str]:
    m = len(p)
    pairs = []
    for i in range(m):
        pairs.append(str(p[i]))
        pairs.append(str(h[i]))
    return [str(m), " ".join(pairs), " ".join(str(x) for x in t)]


def write_in(path: Path, cases: list[tuple[list[int], list[int], list[int]]]) -> None:
    lines = [str(len(cases))]
    for p, h, t in cases:
        lines.extend(fmt_case(p, h, t))
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, cases: list[tuple[list[int], list[int], list[int]]]) -> None:
    ans = [("YES" if can_match(p, h, t) else "NO") for p, h, t in cases]
    path.write_bytes(("\n".join(ans) + "\n").encode("utf-8"))


def dump(idx: int, cases: list[tuple[list[int], list[int], list[int]]]) -> None:
    write_in(DATA / f"{idx}.in", cases)
    write_out(DATA / f"{idx}.out", cases)


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
    text = """# P5465 测例说明

输入：第一行 $q$，每组三行（$m$、交错的 $p/h$、目标 $t$）。输出每组一行 YES/NO。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。YES / NO / YES。
- 2：四级样例 2。单条 YES，逆热度链 NO。
- 3：$m=1$ 且对不齐，NO。
- 4：质量相同，任意热度都可比，目标是置换，YES。
- 5：全局多重集相同但两个不可比块，卡「只比多重集」。
- 6：完全可比链，目标任意重排，YES。
- 7：重复热度。
- 8：随机小数据。
- 9：$m=10^5$ 递增可比，压测。
- 10：$m=10^5$ 逆热度，目标反过来，NO。

hack 点：只查全局多重集、输出 Yes、把不可比点连边、漏掉质量相同的点。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    dump(
        1,
        [
            ([1, 2], [1, 3], [3, 1]),
            ([1, 2], [5, 1], [1, 5]),
            ([1, 2, 3], [4, 1, 5], [1, 4, 5]),
        ],
    )
    dump(
        2,
        [
            ([7], [7], [7]),
            ([1, 2, 3], [5, 3, 1], [1, 3, 5]),
        ],
    )
    dump(3, [([9], [4], [5])])
    dump(4, [([3, 3, 3], [9, 1, 5], [1, 5, 9])])
    dump(
        5,
        [
            (
                [1, 2, 10, 11],
                [8, 7, 1, 2],
                [7, 8, 2, 1],
            )
        ],
    )
    dump(6, [([1, 2, 3, 4], [1, 2, 3, 4], [4, 1, 3, 2])])
    dump(7, [([1, 2, 2, 3], [4, 4, 1, 5], [4, 1, 5, 4])])
    p = [RNG.randint(1, 20) for _ in range(12)]
    h = [RNG.randint(1, 20) for _ in range(12)]
    t = h[:]
    RNG.shuffle(t)
    dump(8, [(p, h, t)])

    n = 100000
    p9 = list(range(1, n + 1))
    h9 = list(range(1, n + 1))
    t9 = h9[::-1]
    dump(9, [(p9, h9, t9)])

    p10 = list(range(1, n + 1))
    h10 = list(range(n, 0, -1))
    t10 = h10[::-1]
    dump(10, [(p10, h10, t10)])

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
