# -*- coding: utf-8 -*-
"""P5489 造数：投篮刷新间隔。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5489)


def best_shot_records(scores: List[int]) -> List[int]:
    cnt = 1
    last = 0
    best = scores[0]
    gap = 0
    for i in range(1, len(scores)):
        if scores[i] > best:
            if i - last > gap:
                gap = i - last
            last = i
            best = scores[i]
            cnt += 1
    return [cnt, gap]


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, scores: List[int]) -> None:
    assert 1 <= len(scores) <= 10**5
    for x in scores:
        assert 1 <= x <= 10**9
    text_in = fmt_arr(scores)
    ans = best_shot_records(scores)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write("[" + str(ans[0]) + ", " + str(ans[1]) + "]\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []

    # 1-3: 题面样例
    cases.append([2, 5, 3, 8, 8, 10])
    cases.append([9, 7, 4])
    cases.append([1, 3, 5, 7])

    # 4: 全部相等，hack 非严格比较
    cases.append([6, 6, 6, 6])

    # 5: 单元素
    cases.append([1000000000])

    # 6: 最长间隔：开头一次、末尾才刷新
    cases.append([3, 1, 1, 1, 1, 1, 9])

    # 7: 中等随机
    cases.append([RNG.randint(1, 1000) for _ in range(200)])

    # 8: 递减后突然新高
    cases.append([50, 40, 30, 20, 10, 5, 80, 70, 90])

    # 9: 大：几乎一直刷新，间隔全是 1
    cases.append(list(range(1, 100001)))

    # 10: 大：仅首尾刷新，卡最大下标差；中间夹相等值 hack >=
    big = [2] + [1] * 99998 + [3]
    cases.append(big)

    assert len(cases) == 10
    assert best_shot_records(cases[0]) == [4, 2]
    assert best_shot_records(cases[1]) == [1, 0]
    assert best_shot_records(cases[2]) == [4, 1]

    for i, scores in enumerate(cases, 1):
        write_case(i, scores)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        scores = json.loads(raw)
        ans = sol.bestShotRecords(scores)
        got = "[" + str(ans[0]) + ", " + str(ans[1]) + "]\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().count(b"\n") == 1

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
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 gen.py。stdin 一行 scores 数组。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    exec_src = Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    shutil.copyfile(exec_src, DATA / "execute.sh")
    print("P5489 data ok:", [best_shot_records(c) for c in cases])


if __name__ == "__main__":
    main()
