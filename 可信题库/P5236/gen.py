# -*- coding: utf-8 -*-
"""P5236 造数：稀疏单元格转 ASCII 表（1-based，只输出出现过的行）。"""
from __future__ import annotations

import random
import string
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5236)


class Cell:
    def __init__(self, rowNum: int, colNum: int, content: str):
        self.rowNum = rowNum
        self.colNum = colNum
        self.content = content


def transform(table: List[Cell]) -> List[str]:
    if not table:
        return []
    rows = sorted({c.rowNum for c in table})
    C = max(c.colNum for c in table)
    grid = {r: [""] * C for r in rows}
    for cell in table:
        grid[cell.rowNum][cell.colNum - 1] = cell.content
    w = 3
    for r in rows:
        for content in grid[r]:
            w = max(w, len(content))

    def pad(s: str) -> str:
        return s + " " * (w - len(s))

    sep = "+" + "+".join(["-" * w] * C) + "+"
    lines = [sep]
    for r in rows:
        lines.append("|" + "|".join(pad(grid[r][c]) for c in range(C)) + "|")
    lines.append(sep)
    return lines


def fmt_in(cells: List[Tuple[int, int, str]]) -> str:
    parts = []
    for r, c, s in cells:
        parts.append(f'[{r},{c},"{s}"]')
    return "[" + ",".join(parts) + "]"


def fmt_out(lines: List[str]) -> str:
    return "[" + ",".join('"' + line + '"' for line in lines) + "]"


def write_case(idx: int, cells: List[Tuple[int, int, str]]) -> None:
    table = [Cell(r, c, s) for r, c, s in cells]
    text_in = fmt_in(cells)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(fmt_out(transform(table)) + "\n")


def rand_word(n: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(RNG.choice(alphabet) for _ in range(n))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[Tuple[int, int, str]]] = []

    # 1: 手稿样例
    cases.append([(1, 3, ""), (3, 2, "")])
    # 2: 题面样例2
    cases.append([(1, 1, "A"), (1, 2, "BC"), (2, 1, "D")])
    # 3: 单格
    cases.append([(1, 1, "")])
    # 4: 覆盖同位置
    cases.append([(1, 1, "x"), (1, 1, "YZ")])
    # 5: 触发宽度 > 3
    cases.append([(1, 1, "abcd"), (1, 2, "e")])
    # 6: 仅右下有内容（中间行不输出）
    cases.append([(5, 4, "hi")])
    # 7: 多行多列稀疏
    cases.append([(1, 1, "a"), (2, 3, "b"), (5, 2, "c")])
    # 8: 中等随机
    cells8 = []
    used = set()
    for _ in range(15):
        while True:
            r, c = RNG.randint(1, 9), RNG.randint(1, 9)
            if (r, c) not in used:
                used.add((r, c))
                break
        cells8.append((r, c, rand_word(RNG.randint(0, 5))))
    cases.append(cells8)
    # 9: 较大坐标
    cases.append([(1, 1, "L"), (20, 15, "R"), (10, 5, "M")])
    # 10: 接近上限
    cells10 = []
    used = set()
    for _ in range(80):
        while True:
            r, c = RNG.randint(1, 40), RNG.randint(1, 40)
            if (r, c) not in used:
                used.add((r, c))
                break
        cells10.append((r, c, rand_word(RNG.randint(0, 8))))
    cases.append(cells10)

    assert len(cases) == 10
    exp1 = transform([Cell(1, 3, ""), Cell(3, 2, "")])
    assert exp1 == [
        "+---+---+---+",
        "|   |   |   |",
        "|   |   |   |",
        "+---+---+---+",
    ], exp1

    for i, cells in enumerate(cases, 1):
        write_case(i, cells)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        triples = eval(raw)
        table = [Cell(r, c, s) for r, c, s in triples]
        got = fmt_out(transform(table)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got[:80], exp[:80])
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 为 `[[r,c,\"s\"],...]`（1-based）。\n",
        encoding="utf-8",
    )
    print("P5236 ok", exp1)


if __name__ == "__main__":
    main()
