# -*- coding: utf-8 -*-
"""P5250 造数：最长连续健康心跳。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5250)


def longest_healthy(beats: List[int]) -> int:
    best = cur = 0
    for x in beats:
        if x == 1:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return best


def fmt_arr(a: List[int]) -> str:
    # 小样例保留空格风格；大数据用紧凑 JSON
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, beats: List[int]) -> None:
    assert 0 <= len(beats) <= 10**5
    for x in beats:
        assert x in (0, 1)
    text_in = fmt_arr(beats)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(longest_healthy(beats)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []

    # 1-3: 题面样例
    cases.append([1, 1, 0, 1, 1, 1])
    cases.append([0, 0, 0])
    cases.append([1])

    # 4: 空数组
    cases.append([])

    # 5: 全 1
    cases.append([1, 1, 1, 1, 1])

    # 6: 最长在开头
    cases.append([1, 1, 1, 0, 1])

    # 7: 交替 0/1
    cases.append([1, 0, 1, 0, 1, 0, 1])

    # 8: 中等随机
    cases.append([RNG.randint(0, 1) for _ in range(200)])

    # 9: 大：单段极长连续 1，夹杂少量 0
    big9 = [0] * 100 + [1] * 50000 + [0] * 100 + [1] * 1000
    cases.append(big9)

    # 10: 大：接近上限 n=1e5，最长在末尾
    big10 = [RNG.randint(0, 1) for _ in range(90000)] + [1] * 10000
    cases.append(big10)

    assert len(cases) == 10
    assert longest_healthy(cases[0]) == 3
    assert longest_healthy(cases[1]) == 0
    assert longest_healthy(cases[2]) == 1

    for i, beats in enumerate(cases, 1):
        write_case(i, beats)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        beats = json.loads(raw) if raw.startswith("[") else eval(raw)
        got = str(sol.longestHealthy(beats)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 一行：beats 数组。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    print("P5250 data ok:", [longest_healthy(c) for c in cases])


if __name__ == "__main__":
    main()
