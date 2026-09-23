# -*- coding: utf-8 -*-
"""P5474 时钟档位校准：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_ops  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547420260919)
MAXV = 10**5


def brute(values: list[int], targets: list[int]) -> list[int]:
    return [sum(abs(v - g) // 2 for v in values) for g in targets]


def write_in(path: Path, values: list[int], targets: list[int]) -> None:
    lines = [
        str(len(values)),
        " ".join(str(x) for x in values),
        str(len(targets)),
        *[str(x) for x in targets],
    ]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[int]) -> None:
    path.write_bytes(("\n".join(str(x) for x in ans) + "\n").encode("utf-8"))


def dump_case(idx: int, values: list[int], targets: list[int], check_brute: bool = False) -> None:
    ans = min_ops(values, targets)
    if check_brute:
        b = brute(values, targets)
        if list(ans) != b:
            raise SystemExit(f"brute mismatch case {idx}: {ans} vs {b}")
    write_in(DATA / f"{idx}.in", values, targets)
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
    text = """# P5474 测例说明

输入：先 $m$ 与偏移数组，再 $k$ 与 $k$ 行目标档。输出 $k$ 行。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。
- 2：四级样例 2。
- 3：$m=1$，目标等于当前偏移，答案 $0$。
- 4：$m=1$，从 $1$ 收到 $10^5$。
- 5：全部相同。含目标就在该值、差 $1$、拉到左端。
- 6：奇偶混合。卡「直接把绝对值之和整除 $2$」：不同奇偶个数大于 $1$ 时会偏大。
- 7：小随机，与 $O(mk)$ 暴力对拍。
- 8：小数据极值。混有 $1$ 与 $10^5$。
- 9：$m=k=10^5$ 随机。卡逐询问扫数组。
- 10：$m=k=10^5$，偏移全是 $1$，目标全是 $10^5$。卡 `int` 溢出，答案约 $5\\times 10^9$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [5, 8, 6, 11], [6, 9, 7], True)
    dump_case(2, [3, 3, 10, 1, 20], [3, 15], True)
    dump_case(3, [7], [7], True)
    dump_case(4, [1], [MAXV], True)
    dump_case(5, [10] * 8, [10, 11, 1], True)
    dump_case(6, [1, 3, 5, 7, 9, 2, 4], [6, 5, 1, 20], True)
    dump_case(
        7,
        [RNG.randint(1, 40) for _ in range(30)],
        [RNG.randint(1, 40) for _ in range(15)],
        True,
    )
    dump_case(8, [1, MAXV, 1, MAXV, 2], [1, MAXV, 2, 50000], True)
    dump_case(
        9,
        [RNG.randint(1, MAXV) for _ in range(MAXV)],
        [RNG.randint(1, MAXV) for _ in range(MAXV)],
    )
    dump_case(10, [1] * MAXV, [MAXV] * MAXV)
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
