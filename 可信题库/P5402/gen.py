# -*- coding: utf-8 -*-
"""造数：烤盘对模具。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(540220260909)


def naive(tray: List[List[str]], stamp: List[List[str]]) -> List[int]:
    m, n = len(tray), len(tray[0])
    a, b = len(stamp), len(stamp[0])
    for i in range(m - a + 1):
        for j in range(n - b + 1):
            ok = True
            for x in range(a):
                for y in range(b):
                    if tray[i + x][j + y] != stamp[x][y]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return [i, j]
    return [-1, -1]


def write_config() -> None:
    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.js
  - template.c
  - execute.sh
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
  - user.js
  - user.c
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
  - js
  - c
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")


def rand_board(m: int, n: int, alphabet: str = "ABCDEF") -> List[List[str]]:
    return [[RNG.choice(alphabet) for _ in range(n)] for _ in range(m)]


def plant(m: int, n: int, a: int, b: int, pos: Tuple[int, int] | None = None) -> Tuple[List[List[str]], List[List[str]], List[int]]:
    tray = rand_board(m, n, "ABCDE")
    if pos is None:
        i0, j0 = RNG.randint(0, m - a), RNG.randint(0, n - b)
    else:
        i0, j0 = pos
    stamp = [row[j0 : j0 + b] for row in tray[i0 : i0 + a]]
    return tray, stamp, naive(tray, stamp)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    s1_t = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    s1_s = [["E", "F"], ["H", "I"]]
    s2_t = [["A", "A", "A"], ["A", "A", "B"]]
    s2_s = [["A", "A"]]
    s3_t = [["A", "B"], ["C", "D"]]
    s3_s = [["B", "A"]]

    t6, s6, _ = plant(8, 9, 3, 4, (2, 3))
    t7 = rand_board(10, 10, "AB")
    s7 = rand_board(2, 3, "XYZ")
    t8, s8, _ = plant(20, 18, 5, 6)

    big_t = [["A"] * 300 for _ in range(300)]
    big_t[180][220] = "Z"
    big_t[180][221] = "Y"
    big_t[181][220] = "X"
    big_t[181][221] = "W"
    big_s = [["Z", "Y"], ["X", "W"]]
    big_miss = [["A"] * 300 for _ in range(300)]
    miss_s = [["B", "B"], ["B", "B"]]

    cases: List[tuple[str, List[List[str]], List[List[str]]]] = [
        ("样例1：右下角子块", s1_t, s1_s),
        ("样例2：多处匹配取最左上", s2_t, s2_s),
        ("样例3：无解且不能旋转", s3_t, s3_s),
        ("单格命中", [["K"]], [["K"]]),
        ("单格未命中", [["K"]], [["Z"]]),
        ("hack：不是第一个窗口", t6, s6),
        ("中等无解", t7, s7),
        ("中等有解", t8, s8),
        ("极限 300 有解", big_t, big_s),
        ("极限 300 无解", big_miss, miss_s),
    ]
    assert len(cases) == 10
    assert sol.findStampPos(s1_t, s1_s) == [1, 1]
    assert sol.findStampPos(s2_t, s2_s) == [0, 0]
    assert sol.findStampPos(s3_t, s3_s) == [-1, -1]
    assert sol.findStampPos(big_t, big_s) == [180, 220]

    readme = [
        "# 测试数据说明",
        "",
        "主造数脚本：`gen.py`。stdin 两行二维数组：tray、stamp。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, tray, stamp) in enumerate(cases, 1):
        m, n = len(tray), len(tray[0])
        a, b = len(stamp), len(stamp[0])
        assert 1 <= m <= 300 and 1 <= n <= 300
        assert 1 <= a <= m and 1 <= b <= n
        text_in = json.dumps(tray) + "\n" + json.dumps(stamp)
        (DATA / f"{i}.in").write_bytes(text_in.encode("utf-8"))
        ans = sol.findStampPos(tray, stamp)
        if m * n * a * b <= 2_000_000:
            assert ans == naive(tray, stamp), (i, ans, naive(tray, stamp))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(ans) + "\n")
        readme.append(f"| {i} | {desc} |")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        lines = raw.decode("utf-8").split("\n")
        tray = json.loads(lines[0])
        stamp = json.loads(lines[1])
        got = json.dumps(sol.findStampPos(tray, stamp)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)

    write_config()
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print("P5402 data ok")


if __name__ == "__main__":
    main()
