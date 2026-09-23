# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5492)


def max_load_drop(loads: List[int]) -> int:
    peak = loads[0]
    ans = 0
    for x in loads:
        if peak - x > ans:
            ans = peak - x
        if x > peak:
            peak = x
    return ans


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, loads: List[int]) -> None:
    assert 1 <= len(loads) <= 10**5
    for x in loads:
        assert 1 <= x <= 10**6
    (DATA / f"{idx}.in").write_bytes(fmt_arr(loads).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(max_load_drop(loads)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        [8, 25, 18, 22, 12, 30, 4],
        [5, 6, 7, 8],
        [100, 20],
        [7],
        [50, 50, 50],
        [9, 1, 8, 2],
        [RNG.randint(1, 1000) for _ in range(200)],
        list(range(1, 301)),
        [10**6] + [1] * 99999,
        [RNG.randint(1, 10**6) for _ in range(10**5)],
    ]
    assert len(cases) == 10
    assert max_load_drop(cases[0]) == 26
    assert max_load_drop(cases[1]) == 0
    assert max_load_drop(cases[2]) == 80

    for i, loads in enumerate(cases, 1):
        write_case(i, loads)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()
    for i in range(1, 11):
        loads = json.loads((DATA / f"{i}.in").read_text(encoding="utf-8"))
        got = str(sol.maxLoadDrop(loads)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp
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
    (DATA / "README.md").write_text("主造数脚本：题目根目录 gen.py。stdin 一行 loads 数组。\n", encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")
    print("P5492 data ok", [max_load_drop(c) for c in cases[:8]])


if __name__ == "__main__":
    main()
