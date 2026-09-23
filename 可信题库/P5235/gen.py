# -*- coding: utf-8 -*-
"""P5235 造数：五子连珠检测。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5235)

Pos = Tuple[int, int]


def has_five(poses: List[List[int]]) -> str:
    s = {(x, y) for x, y in poses}
    dirs = ((1, 0), (0, 1), (1, 1), (1, -1))
    for x, y in s:
        for dx, dy in dirs:
            if (x - dx, y - dy) in s:
                continue
            cnt = 0
            cx, cy = x, y
            while (cx, cy) in s:
                cnt += 1
                if cnt >= 5:
                    return "YES"
                cx += dx
                cy += dy
    return "NO"


def fmt(poses: List[List[int]]) -> str:
    return "[" + ",".join(f"[{x},{y}]" for x, y in poses) + "]"


def write_case(idx: int, poses: List[List[int]]) -> None:
    assert 1 <= len(poses) <= 361
    seen = set()
    for x, y in poses:
        assert 0 <= x <= 18 and 0 <= y <= 18
        assert (x, y) not in seen
        seen.add((x, y))
    text_in = fmt(poses)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write('"' + has_five(poses) + '"\n')


def line_seg(x0: int, y0: int, dx: int, dy: int, k: int) -> List[List[int]]:
    return [[x0 + i * dx, y0 + i * dy] for i in range(k)]


def rand_noise(exclude: set, m: int) -> List[List[int]]:
    out = []
    while len(out) < m:
        x, y = RNG.randint(0, 18), RNG.randint(0, 18)
        if (x, y) in exclude:
            continue
        exclude.add((x, y))
        out.append([x, y])
    return out


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[List[int]]] = []

    # 1-3: 题面样例
    cases.append([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]])
    cases.append([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
    cases.append([[0, 0], [1, 0], [2, 0], [4, 0], [5, 0]])

    # 4: n<5 → NO
    cases.append([[0, 0], [1, 0], [2, 0], [3, 0]])

    # 5: 竖直五连
    cases.append([[7, 3], [7, 4], [7, 5], [7, 6], [7, 7]])

    # 6: 副对角 (1,-1)
    cases.append([[10, 10], [11, 9], [12, 8], [13, 7], [14, 6]])

    # 7: 六连仍 YES（卡「必须恰好 5」假解）
    cases.append(line_seg(2, 5, 1, 0, 6))

    # 8: 多噪声 + 隐藏五连
    base = line_seg(0, 18, 1, -1, 5)
    ex = {(x, y) for x, y in base}
    cases.append(base + rand_noise(ex, 40))

    # 9: 大板无五连（随机稀疏）
    ex = set()
    sparse = rand_noise(ex, 80)
    # 确保无五：用 has_five 过滤，不行就重采样
    for _ in range(20):
        if has_five(sparse) == "NO":
            break
        ex = set()
        sparse = rand_noise(ex, 80)
    assert has_five(sparse) == "NO"
    cases.append(sparse)

    # 10: 接近满盘但含一条五连
    full = [[x, y] for y in range(19) for x in range(19)]
    # 满盘必有大量五连
    cases.append(full)

    assert len(cases) == 10
    assert has_five(cases[0]) == "YES"
    assert has_five(cases[1]) == "YES"
    assert has_five(cases[2]) == "NO"
    assert has_five(cases[3]) == "NO"
    assert has_five(cases[6]) == "YES"
    assert has_five(cases[9]) == "YES"

    for i, poses in enumerate(cases, 1):
        write_case(i, poses)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        poses = eval(raw)
        got = '"' + has_five(poses) + '"\n'
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
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
        "主造数脚本：题目根目录 `gen.py`。测例 stdin 为一行 `[[x,y],...]`。\n",
        encoding="utf-8",
    )
    print("P5235 data ok:", [has_five(c) for c in cases])


if __name__ == "__main__":
    main()
