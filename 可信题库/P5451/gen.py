# -*- coding: utf-8 -*-
"""P5451 造数：模具份数凑公约。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5451)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 30:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, arr: List[int]) -> None:
    text_in = fmt_arr(arr)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []

    # 1-3 样例
    cases.append([1, 1])
    cases.append([4, 8])
    cases.append([3, 11])

    # 4: 已有公共偶因子
    cases.append([2, 4, 6, 9])

    # 5: 全奇数互质，答案 2
    cases.append([1, 3, 5, 7, 11])

    # 6: 加一次即可（7+1=8 与 8 撞偶）
    cases.append([7, 8])

    # 7: 两个相同大质数
    cases.append([97, 97])

    # 8: 中等随机
    cases.append([RNG.randint(1, 500) for _ in range(80)])

    # 9: 大：答案 0，大量偶数
    big9 = [RNG.choice([2, 4, 6, 8, 10, 12]) for _ in range(100000)]
    cases.append(big9)

    # 10: 大：逼近上限，多为奇数互素风格，答案倾向 2
    odds = [1, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    big10 = [RNG.choice(odds) for _ in range(100000)]
    # 夹杂一个大奇数
    big10[0] = 199999
    cases.append(big10)

    assert len(cases) == 10

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    assert sol.minShareOps(cases[0]) == 2
    assert sol.minShareOps(cases[1]) == 0
    assert sol.minShareOps(cases[2]) == 1

    for i, arr in enumerate(cases, 1):
        write_case(i, arr)
        got = sol.minShareOps(arr)
        (DATA / f"{i}.out").write_bytes((str(got) + "\n").encode("utf-8"))

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        arr = json.loads(raw)
        got = str(sol.minShareOps(arr)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

    cfg = """type: default
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
      - input: 1.in
        output: 1.out
      - input: 2.in
        output: 2.out
      - input: 3.in
        output: 3.out
      - input: 4.in
        output: 4.out
      - input: 5.in
        output: 5.out
      - input: 6.in
        output: 6.out
      - input: 7.in
        output: 7.out
      - input: 8.in
        output: 8.out
      - input: 9.in
        output: 9.out
      - input: 10.in
        output: 10.out
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
  - js
  - c
"""
    (DATA / "config.yaml").write_text(cfg, encoding="utf-8")
    (DATA / "README.md").write_text(
        "stdin 为一行整型数组，与题面样例同构。\n", encoding="utf-8"
    )
    print("P5451 gen ok")


if __name__ == "__main__":
    main()
