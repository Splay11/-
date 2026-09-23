# -*- coding: utf-8 -*-
"""P7010 造数：HSM 密钥批次划分 DP。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7010)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")


def solve(sens: List[int], base: int, k: int) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.Solution().minRotateCost(sens, base, k)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, sens: List[int], base: int, k: int) -> None:
    n = len(sens)
    assert 1 <= n <= 200
    assert 1 <= k <= n
    assert 1 <= base <= 10**9
    for x in sens:
        assert 1 <= x <= 10**4
    text_in = fmt_arr(sens) + "\n" + str(base) + "\n" + str(k)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(sens, base, k)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[List[int], int, int]] = []

    cases.append(([1, 3, 2], 5, 3))
    cases.append(([2, 2], 10, 1))
    cases.append(([1, 1, 1], 100, 3))

    # 4 单元素
    cases.append(([7], 1, 1))

    # 5 k=n → 可全拆；base 很小应拆
    cases.append(([10, 1], 1, 2))

    # 6 k=1 必须一整段
    cases.append(([9, 8, 7, 6], 3, 1))

    # 7 中等随机
    s7 = [RNG.randint(1, 100) for _ in range(40)]
    cases.append((s7, RNG.randint(1, 50), RNG.randint(1, 40)))

    # 8 hack：大 base 应合并，小 k 限制
    cases.append(([1, 10000, 1, 10000], 10**9, 2))

    # 9 较大
    s9 = [RNG.randint(1, 10000) for _ in range(120)]
    cases.append((s9, RNG.randint(1, 10**6), RNG.randint(10, 120)))

    # 10 极限
    s10 = [RNG.randint(1, 10000) for _ in range(200)]
    cases.append((s10, 10**9, 200))

    assert len(cases) == 10
    assert solve(*cases[0]) == 20
    assert solve(*cases[1]) == 18
    assert solve(*cases[2]) == 109

    for i, c in enumerate(cases, 1):
        write_case(i, *c)

    for i in range(1, 11):
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n") and outb.count(b"\n") == 1

    cases_yaml = "\n".join(f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11))
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.c
  - compile.sh
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
        "主造数脚本：题目根目录 `gen.py`。stdin 三行：sens、baseCost、maxBatches。\n"
        "5 卡「整批」贪心；8 大 baseCost 溢出风险与批次数限制。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    print("P7010 data ok")


if __name__ == "__main__":
    main()
