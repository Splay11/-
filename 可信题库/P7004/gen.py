# -*- coding: utf-8 -*-
"""P7004 造数：最小归档容量（二分 + 连续整包装箱）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7004)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")


def need(logs: List[int], cap: int) -> int:
    days = 1
    cur = 0
    for x in logs:
        if cur + x > cap:
            days += 1
            cur = 0
        cur += x
    return days


def min_archive_cap(logs: List[int], limit_days: int) -> int:
    lo, hi = max(logs), sum(logs)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(logs, mid) <= limit_days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, logs: List[int], limit_days: int) -> None:
    n = len(logs)
    assert 1 <= n <= 5 * 10**4
    assert 1 <= limit_days <= n
    for x in logs:
        assert 1 <= x <= 10**9
    text_in = fmt_arr(logs) + "\n" + str(limit_days)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(min_archive_cap(logs, limit_days)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Tuple[List[int], int]] = []

    # 1-3: 样例
    cases.append(([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))
    cases.append(([3, 2, 2, 4, 1, 4], 3))
    cases.append(([1, 2, 3, 1, 1], 4))

    # 4: 单包
    cases.append(([7], 1))

    # 5: limitDays == n → 答案为 max
    cases.append(([5, 1, 9, 2], 4))

    # 6: limitDays == 1 → 答案为 sum
    cases.append(([1, 2, 3, 4], 1))

    # 7: 中等随机
    logs7 = [RNG.randint(1, 1000) for _ in range(80)]
    cases.append((logs7, RNG.randint(1, 80)))

    # 8: hack 错误贪心/边界 mid；大值
    cases.append(([10**9, 1, 1], 2))

    # 9: 大 n
    logs9 = [RNG.randint(1, 10**6) for _ in range(20000)]
    cases.append((logs9, RNG.randint(1, 20000)))

    # 10: 极限
    logs10 = [RNG.randint(1, 10**9) for _ in range(50000)]
    cases.append((logs10, RNG.randint(1000, 50000)))

    assert len(cases) == 10
    assert min_archive_cap(*cases[0]) == 15
    assert min_archive_cap(*cases[1]) == 6
    assert min_archive_cap(*cases[2]) == 3

    for i, (logs, d) in enumerate(cases, 1):
        write_case(i, logs, d)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = [ln for ln in raw.split("\n") if ln.strip() != ""]
        logs = json.loads(lines[0])
        limit_days = int(lines[1])
        got = str(sol.minArchiveCap(logs, limit_days)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 两行：logs、limitDays。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    print("P7004 data ok:", [min_archive_cap(*c) for c in cases[:3]])


if __name__ == "__main__":
    main()
