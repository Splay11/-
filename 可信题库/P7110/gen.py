# -*- coding: utf-8 -*-
"""P7110 造数：合规科目过关最短天数（二分 + 贪心）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7110)
PM = ROOT.parent.parent
COMPILE_SH = PM / "compile.sh"
EXECUTE_SH = PM / "核心代码模式模板" / "execute.sh"


def solve(slots: List[int], prep: List[int]) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution().minPassDays(slots, prep)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, slots: List[int], prep: List[int]) -> None:
    n, m = len(slots), len(prep)
    assert 1 <= n <= 10**5 and 1 <= m <= 10**5
    for x in slots:
        assert 0 <= x <= m
    for x in prep:
        assert 1 <= x <= 10**5
    text_in = fmt_arr(slots) + "\n" + fmt_arr(prep)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(slots, prep)) + "\n")


def rand_case(n: int, m: int) -> Tuple[List[int], List[int]]:
    slots = [RNG.randint(0, m) for _ in range(n)]
    # 保证每门至少出现一次，避免大量 -1
    for t in range(1, m + 1):
        slots[RNG.randint(0, n - 1)] = t
    prep = [RNG.randint(1, max(1, n // max(1, m))) for _ in range(m)]
    return slots, prep


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[List[int], List[int]]] = []
    cases.append(([0, 1, 0, 2, 1, 0, 2], [2, 1]))
    cases.append(([0, 0, 1, 2, 3, 0, 2, 0, 1, 2], [1, 1, 4]))
    cases.append(([1, 1, 1, 1, 1], [5]))
    cases.append(([0, 1], [1]))
    cases.append(([1], [1]))
    # 全部能考但复习太大
    cases.append(([1, 2, 1, 2, 1, 2], [10, 10]))
    cases.append(rand_case(40, 5))
    # hack：必须用「可考日拿来复习」才能过
    cases.append(([1, 1, 1, 1], [2]))
    # 对 [1,1,1,1] prep=[2]：最后考在 day3，前 3 天只有 3 个非考日？ days 0,1,2 若 day3 考试，free=3 >=2 -> ok, ans?
    # check: last[1]=3, free on 0,1,2 =3 >=2, day3 exam -> ok with 4 days. With 3 days last=2, free=2>=2, exam day2 -> ok ans=3
    cases.append(rand_case(2000, 50))
    cases.append(rand_case(100000, 200))

    assert len(cases) == 10
    assert solve(*cases[0]) == 5
    assert solve(*cases[1]) == 9
    assert solve(*cases[2]) == -1

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
        "主造数脚本：题目根目录 `gen.py`。stdin 两行：slots、prep。\n"
        "二分天数 + 末次考试日贪心；8 卡「可考日也要当复习」；10 压 n=1e5。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    shutil.copyfile(EXECUTE_SH, DATA / "execute.sh")
    print("P7110 data ok")


if __name__ == "__main__":
    main()
