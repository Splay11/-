# -*- coding: utf-8 -*-
"""P5251 造数：首次重复用户。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5251)


def first_duplicate(users: List[int]) -> int:
    seen = set()
    for u in users:
        if u in seen:
            return u
        seen.add(u)
    return -1


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, users: List[int]) -> None:
    assert 0 <= len(users) <= 10**5
    for u in users:
        assert 1 <= u <= 10**9
    text_in = fmt_arr(users)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(first_duplicate(users)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []

    # 1-3: 题面样例
    cases.append([3, 1, 4, 1, 5])
    cases.append([1, 2, 3, 4])
    cases.append([7, 7])

    # 4: 空
    cases.append([])

    # 5: 单元素
    cases.append([42])

    # 6: 末尾才重复（hack：取最后一个重复而非第一个）
    cases.append([1, 2, 3, 4, 5, 2])

    # 7: 多个重复，答案应是最早触发的
    cases.append([9, 8, 7, 8, 9, 7])

    # 8: 中等：前半唯一，中段出现重复
    mid = list(range(1, 101)) + [50] + list(range(101, 151))
    cases.append(mid)

    # 9: 大：无重复
    cases.append(list(range(1, 50001)))

    # 10: 大：接近末尾才首次重复
    big = list(range(1, 80001)) + [12345]
    cases.append(big)

    assert len(cases) == 10
    assert first_duplicate(cases[0]) == 1
    assert first_duplicate(cases[1]) == -1
    assert first_duplicate(cases[2]) == 7
    assert first_duplicate(cases[5]) == 2
    assert first_duplicate(cases[6]) == 8

    for i, users in enumerate(cases, 1):
        write_case(i, users)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        users = json.loads(raw)
        got = str(sol.firstDuplicate(users)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 一行：users 数组。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    print("P5251 data ok:", [first_duplicate(c) for c in cases])


if __name__ == "__main__":
    main()
