# -*- coding: utf-8 -*-
"""P7111 造数：风控探针存活窗口（后缀 DP + 前缀和二分）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7111)
PM = ROOT.parent.parent
COMPILE_SH = PM / "compile.sh"
EXECUTE_SH = PM / "核心代码模式模板" / "execute.sh"


def solve(loads: List[int], cap: int) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution().countLiveWindows(loads, cap)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, loads: List[int], cap: int) -> None:
    n = len(loads)
    assert 1 <= n <= 2 * 10**5
    assert 1 <= cap <= 10**9
    for x in loads:
        assert 1 <= x <= 10**9
    text_in = fmt_arr(loads) + "\n" + str(cap)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(loads, cap)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[List[int], int]] = []
    cases.append(([1, 1, 1, 1], 2))
    cases.append(([1, 2, 3], 2))
    cases.append(([10], 6))
    cases.append(([1, 2, 1, 4, 3, 8], 3))
    cases.append(
        ([999999999, 999999998, 1000000000, 1000000000, 500000000], 999999999)
    )
    cases.append(([1], 1))
    # 全不超阈 → 全部 n(n+1)/2
    cases.append(([1, 1, 1, 1, 1], 100))
    # hack：多次清零链
    cases.append(([5, 5, 5, 5], 4))
    s9 = [RNG.randint(1, 10**6) for _ in range(5000)]
    cases.append((s9, RNG.randint(1, 10**9)))
    s10 = [RNG.randint(1, 10**9) for _ in range(200000)]
    cases.append((s10, RNG.randint(1, 10**9)))

    assert len(cases) == 10
    assert solve(*cases[0]) == 8
    assert solve(*cases[1]) == 2
    assert solve(*cases[2]) == 0
    assert solve(*cases[3]) == 10
    assert solve(*cases[4]) == 7
    assert solve(*cases[6]) == 15

    for i, c in enumerate(cases, 1):
        write_case(i, *c)

    for i in range(1, 11):
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n") and outb.count(b"\n") == 1

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.c
  - compile.sh
  - execute.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
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
  - c
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 两行：loads、cap。\n"
        "8 多次清零；10 压 n=2e5。假解：只数「整段和 ≤ cap」会错。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    shutil.copyfile(EXECUTE_SH, DATA / "execute.sh")
    print("P7111 data ok")


if __name__ == "__main__":
    main()
