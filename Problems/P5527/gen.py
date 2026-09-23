# -*- coding: utf-8 -*-
"""生成 P5527 测试数据：样例在前，末两组近上限。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"
RNG = random.Random(5527)

CONFIG = """type: default
time: 2s
memory: 256m
subtasks:
  - score: 100
    type: sum
    cases:
{cases}
langs:
  - py.py3
  - java
  - cc.cc14o2
"""


def write_case(idx: int, content: str) -> None:
    text = content.rstrip("\n")
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))
    proc = subprocess.run(
        [sys.executable, str(STD)],
        input=text + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout.replace("\r\n", "\n")
    out = out.rstrip("\n") + "\n"
    (DATA / f"{idx}.out").write_bytes(out.encode("utf-8"))


def grid_str(n: int, m: int, g: list[list[int]]) -> str:
    lines = [f"{n} {m}"]
    for row in g:
        lines.append(" ".join(map(str, row)))
    return "\n".join(lines)


def empty_grid(n: int, m: int) -> list[list[int]]:
    return [[0] * m for _ in range(n)]


def blocked_path(n: int, m: int) -> list[list[int]]:
    g = empty_grid(n, m)
    # 竖墙挡住，仅留一条缝或完全封死
    for i in range(n):
        g[i][m // 2] = 1
    g[0][0] = 0
    g[n - 1][m - 1] = 0
    return g


def maze_with_path(n: int, m: int, walls: float = 0.3) -> list[list[int]]:
    g = empty_grid(n, m)
    for i in range(n):
        for j in range(m):
            if (i, j) in ((0, 0), (n - 1, m - 1)):
                continue
            if RNG.random() < walls:
                g[i][j] = 1
    # 保证一条右下路径畅通
    x = y = 0
    while x < n - 1 or y < m - 1:
        if x == n - 1:
            y += 1
        elif y == m - 1:
            x += 1
        elif RNG.random() < 0.5:
            x += 1
        else:
            y += 1
        g[x][y] = 0
    return g


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    s1 = """4 2
0 0
0 0
0 0
0 0"""
    s2 = """2 3
0 0 0
0 0 0"""
    g3 = empty_grid(2, 2)
    g4 = [[0, 1], [1, 0]]  # 不可达
    g5 = maze_with_path(5, 5, 0.4)
    g6 = blocked_path(6, 6)
    g7 = maze_with_path(20, 20, 0.35)
    g8 = empty_grid(50, 50)
    g9 = maze_with_path(500, 500, 0.25)
    g10 = empty_grid(500, 500)

    cases = [
        s1,
        s2,
        grid_str(2, 2, g3),
        grid_str(2, 2, g4),
        grid_str(5, 5, g5),
        grid_str(6, 6, g6),
        grid_str(20, 20, g7),
        grid_str(50, 50, g8),
        grid_str(500, 500, g9),
        grid_str(500, 500, g10),
    ]
    assert len(cases) == 10
    for i, c in enumerate(cases, 1):
        write_case(i, c)

    case_lines = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    cfg = CONFIG.format(cases=case_lines)
    (ROOT / "config.yaml").write_text(cfg, encoding="utf-8")
    (DATA / "config.yaml").write_text(cfg, encoding="utf-8")
    print("P5527 gen done")


if __name__ == "__main__":
    main()
