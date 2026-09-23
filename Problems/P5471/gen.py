# -*- coding: utf-8 -*-
"""P5471 时窗巡回最短：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_tour  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547120260918)


def write_in(path: Path, m: int, lo: list[int], hi: list[int], dur: list[list[int]]) -> None:
    lines = [str(m)]
    for p in range(m):
        lines.append(f"{lo[p]} {hi[p]}")
    for p in range(m):
        lines.append(" ".join(str(x) for x in dur[p]))
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def dump_case(idx: int, lo: list[int], hi: list[int], dur: list[list[int]]) -> int:
    m = len(lo)
    ans = min_tour(m, lo, hi, dur)
    write_in(DATA / f"{idx}.in", m, lo, hi, dur)
    write_out(DATA / f"{idx}.out", ans)
    return ans


def ident(m: int, val: int = 8) -> list[list[int]]:
    dur = [[val] * m for _ in range(m)]
    for i in range(m):
        dur[i][i] = 0
    return dur


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 1s
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


def write_readme(answers: dict[int, int]) -> None:
    text = """# P5471 测例说明

输入：首行 $m$，随后 $m$ 行 $lo\\ hi$，再 $m$ 行 $m$ 列耗时矩阵。输出一个整数：最短回到仓站的时刻，或 $-1$。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。最优 $0\\to1\\to2\\to3\\to0$，答案 $36$。
- 2：二级样例 2。三位客户窗口都挤在 $[5,12]$，无解。
- 3：$m=2$ 最小规模。只有一位客户，必须等候。
- 4：对称矩阵、窗口极宽。卡「输出行驶之和却忘了回仓」或下标从 $1$ 开始读。
- 5：必须早到等候。卡「到达时刻小于 $lo$ 直接判非法」或不等待。
- 6：不对称耗时。后访问回程便宜的那一站才优。卡「把矩阵当对称」。
- 7：最近邻贪心会先去近的客户，随后迟到；正解另一条顺序可行。
- 8：截止日期更早的客户 $2$ 若先走，再去 $1$ 会迟到；正解先走 $1$。卡 EDF 贪心。
- 9：$m=15$ 窗口宽松、随机不对称矩阵。压测状压上界，必有解。
- 10：$m=15$ 后半段客户窗口极窄且互走很慢，无解。卡「忽略窗口仍输出一个巡回时长」。
"""
    extra = "\n生成答案：\n" + "\n".join(f"- {i}：{answers[i]}" for i in range(1, 11)) + "\n"
    (DATA / "README.md").write_text(text + extra, encoding="utf-8")


def large_feasible(m: int, rng: random.Random) -> tuple[list[int], list[int], list[list[int]]]:
    lo = [0] * m
    hi = [1440] * m
    dur = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            dur[i][j] = rng.randint(1, 20)
    return lo, hi, dur


def large_impossible(m: int) -> tuple[list[int], list[int], list[list[int]]]:
    lo = [0] * m
    hi = [1440] * m
    for i in range(1, m):
        lo[i] = 0
        hi[i] = 8
    dur = ident(m, 30)
    return lo, hi, dur


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    answers: dict[int, int] = {}

    # 1 二级样例 1
    answers[1] = dump_case(
        1,
        [0, 6, 20, 14],
        [1440, 18, 45, 28],
        [
            [0, 4, 18, 8],
            [6, 0, 9, 20],
            [10, 12, 0, 7],
            [9, 16, 11, 0],
        ],
    )

    # 2 二级样例 2
    answers[2] = dump_case(
        2,
        [0, 5, 5, 5],
        [1440, 12, 12, 12],
        [
            [0, 4, 4, 4],
            [4, 0, 10, 10],
            [4, 10, 0, 10],
            [4, 10, 10, 0],
        ],
    )

    # 3 m=2，必须等候
    answers[3] = dump_case(
        3,
        [0, 10],
        [1440, 20],
        [[0, 3], [4, 0]],
    )

    # 4 对称宽窗口
    answers[4] = dump_case(
        4,
        [0, 0, 0, 0],
        [1440, 1440, 1440, 1440],
        [
            [0, 5, 5, 5],
            [5, 0, 5, 5],
            [5, 5, 0, 5],
            [5, 5, 5, 0],
        ],
    )

    # 5 早到必须等：去客户 1 只需 2，但窗口从 15 才开
    answers[5] = dump_case(
        5,
        [0, 15, 0],
        [1440, 40, 1440],
        [
            [0, 2, 8],
            [3, 0, 4],
            [8, 4, 0],
        ],
    )

    # 6 不对称：2 回仓很便宜，应把 2 放最后
    answers[6] = dump_case(
        6,
        [0, 0, 0],
        [1440, 1440, 1440],
        [
            [0, 5, 50],
            [80, 0, 5],
            [5, 80, 0],
        ],
    )

    # 7 最近邻：仓站到 1 更近，但 1 之后去 2 会迟到；应先去 2
    answers[7] = dump_case(
        7,
        [0, 0, 8],
        [1440, 40, 12],
        [
            [0, 1, 4],
            [1, 0, 20],
            [4, 20, 0],
        ],
    )

    # 8 EDF：客户 2 截止日期更早，先去 2 再去 1 会迟到；应先去 1
    answers[8] = dump_case(
        8,
        [0, 0, 20],
        [1440, 100, 30],
        [
            [0, 5, 25],
            [5, 0, 20],
            [5, 80, 0],
        ],
    )

    # 9 上限可行
    lo9, hi9, dur9 = large_feasible(15, RNG)
    answers[9] = dump_case(9, lo9, hi9, dur9)

    # 10 上限无解
    lo10, hi10, dur10 = large_impossible(15)
    answers[10] = dump_case(10, lo10, hi10, dur10)

    write_config()
    write_readme(answers)
    print("answers", answers)


if __name__ == "__main__":
    main()
