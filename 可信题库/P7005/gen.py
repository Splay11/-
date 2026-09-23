# -*- coding: utf-8 -*-
"""P7005 造数：累计峰值风险（单调栈贡献）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7005)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")
MOD = 10**9 + 7


def sum_peak_risk(loads: List[int]) -> int:
    n = len(loads)
    left = [0] * n
    right = [0] * n
    st: List[int] = []
    for i in range(n):
        while st and loads[st[-1]] <= loads[i]:
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st.clear()
    for i in range(n - 1, -1, -1):
        while st and loads[st[-1]] < loads[i]:
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    ans = 0
    for i in range(n):
        ans = (ans + loads[i] * left[i] * right[i]) % MOD
    return ans


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, loads: List[int]) -> None:
    n = len(loads)
    assert 1 <= n <= 10**5
    for x in loads:
        assert 1 <= x <= 10**9
    text_in = fmt_arr(loads)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(sum_peak_risk(loads)) + "\n")


def brute(loads: List[int]) -> int:
    n = len(loads)
    ans = 0
    for i in range(n):
        mx = 0
        for j in range(i, n):
            mx = max(mx, loads[j])
            ans = (ans + mx) % MOD
    return ans


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[int]] = []

    # 1-3: 样例
    cases.append([1, 2, 3])
    cases.append([3, 1, 2])
    cases.append([2, 2])

    # 4: 单点
    cases.append([7])

    # 5: 严格递增
    cases.append([1, 2, 3, 4, 5])

    # 6: 严格递减
    cases.append([5, 4, 3, 2, 1])

    # 7: 中等随机
    cases.append([RNG.randint(1, 1000) for _ in range(80)])

    # 8: hack 相等峰值归属（左严格 / 右非严格）
    cases.append([2, 2, 2, 3, 3, 1, 1])

    # 9: 较大 n
    cases.append([RNG.randint(1, 10**6) for _ in range(50000)])

    # 10: 极限 n + 大值
    cases.append([RNG.randint(1, 10**9) for _ in range(100000)])

    assert len(cases) == 10
    assert sum_peak_risk(cases[0]) == 14
    assert sum_peak_risk(cases[1]) == 14
    assert sum_peak_risk(cases[2]) == 6
    for c in cases[:8]:
        assert sum_peak_risk(c) == brute(c), c

    for i, loads in enumerate(cases, 1):
        write_case(i, loads)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        loads = json.loads(raw.split("\n")[0])
        got = str(sol.sumPeakRisk(loads)) + "\n"
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
        "主造数脚本：题目根目录 `gen.py`。stdin 一行：loads 数组（与样例同形）。输出一个整数。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    print("P7005 data ok:", [sum_peak_risk(c) for c in cases[:3]])


if __name__ == "__main__":
    main()
