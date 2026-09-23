# -*- coding: utf-8 -*-
"""P7001 造数：直播峰值并发（扫描线）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7001)


def peak_concurrent(starts: List[int], ends: List[int]) -> int:
    starts = sorted(starts)
    ends = sorted(ends)
    i = j = 0
    cur = ans = 0
    n = len(starts)
    while i < n:
        if starts[i] < ends[j]:
            cur += 1
            if cur > ans:
                ans = cur
            i += 1
        else:
            cur -= 1
            j += 1
    return ans


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 30:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, starts: List[int], ends: List[int]) -> None:
    assert len(starts) == len(ends) >= 1
    n = len(starts)
    assert n <= 10**4
    for s, e in zip(starts, ends):
        assert 0 <= s < e <= 10**5
    text_in = fmt_arr(starts) + "\n" + fmt_arr(ends)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(peak_concurrent(starts, ends)) + "\n")


def rand_intervals(n: int, tmax: int = 10**5) -> Tuple[List[int], List[int]]:
    starts, ends = [], []
    for _ in range(n):
        s = RNG.randint(0, tmax - 1)
        e = RNG.randint(s + 1, tmax)
        starts.append(s)
        ends.append(e)
    return starts, ends


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[List[int], List[int]]] = []

    # 1-3: 样例
    cases.append(([1, 2, 3], [3, 5, 4]))
    cases.append(([1, 2], [2, 3]))
    cases.append(([0, 0, 0], [10, 10, 10]))

    # 4: 单场
    cases.append(([5], [6]))

    # 5: 全部首尾相接（半开不重叠）→ 1
    cases.append(([0, 1, 2, 3], [1, 2, 3, 4]))

    # 6: 嵌套
    cases.append(([0, 1, 2], [10, 9, 8]))

    # 7: 中等随机
    cases.append(rand_intervals(50, 1000))

    # 8: 多段重叠峰值
    cases.append(([0, 0, 0, 5, 5], [5, 5, 5, 10, 10]))

    # 9: 大 n
    cases.append(rand_intervals(8000, 10**5))

    # 10: 极限全重叠
    cases.append(([0] * 10000, [10**5] * 10000))

    assert len(cases) == 10
    assert peak_concurrent(*cases[0]) == 2
    assert peak_concurrent(*cases[1]) == 1
    assert peak_concurrent(*cases[2]) == 3

    for i, (st, en) in enumerate(cases, 1):
        write_case(i, st, en)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = [ln for ln in raw.split("\n") if ln.strip() != ""]
        starts = json.loads(lines[0])
        ends = json.loads(lines[1])
        got = str(sol.peakConcurrent(starts, ends)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 两行：starts、ends。\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    print("P7001 data ok:", [peak_concurrent(*c) for c in cases])


if __name__ == "__main__":
    main()
