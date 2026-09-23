# -*- coding: utf-8 -*-
"""P5244 造数：弹性算力最小费用（变更次数限制 DP）。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(524420260815)
N_MAX = 80
LOAD_MAX = 40
COST_MAX = 1000


def solve(load: List[int], runCost: int, changeCost: int, maxChanges: int) -> int:
    n = len(load)
    M = max(load) if load else 0
    INF = 10**18
    prev = [{} for _ in range(maxChanges + 1)]
    prev[0][0] = 0
    for i in range(n):
        cur = [{} for _ in range(maxChanges + 1)]
        for c in range(maxChanges + 1):
            for p, cost in prev[c].items():
                for x in range(load[i], M + 1):
                    nc = c + (0 if x == p else 1)
                    if nc > maxChanges:
                        continue
                    nc_cost = cost + x * runCost + abs(x - p) * changeCost
                    if x not in cur[nc] or nc_cost < cur[nc][x]:
                        cur[nc][x] = nc_cost
        prev = cur
    ans = INF
    for c in range(maxChanges + 1):
        if prev[c]:
            ans = min(ans, min(prev[c].values()))
    return ans


def fmt_arr(a: List[int]) -> str:
    return "[" + ", ".join(str(x) for x in a) + "]"


def fmt_in(load: List[int], runCost: int, changeCost: int, maxChanges: int) -> str:
    return f"{fmt_arr(load)}\n{runCost}\n{changeCost}\n{maxChanges}"


def validate(load: List[int], runCost: int, changeCost: int, maxChanges: int) -> None:
    n = len(load)
    assert 1 <= n <= N_MAX
    assert all(0 <= x <= LOAD_MAX for x in load)
    assert 1 <= runCost <= COST_MAX
    assert 1 <= changeCost <= COST_MAX
    assert 1 <= maxChanges <= n
    # 保证有解：至少可在第 0 天拉到 max(load) 并保持
    assert maxChanges >= 1 or max(load) == 0


def write_cases(cases: List[Tuple[str, List[int], int, int, int]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    readme = [
        "# P5244 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 四行：`load` / `runCost` / `changeCost` / `maxChanges`，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, load, runCost, changeCost, maxChanges) in enumerate(cases, 1):
        validate(load, runCost, changeCost, maxChanges)
        ans = solve(load, runCost, changeCost, maxChanges)
        text_in = fmt_in(load, runCost, changeCost, maxChanges)
        (DATA / f"{i}.in").write_bytes(text_in.encode("utf-8"))
        with open(DATA / f"{i}.out", "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{ans}\n")
        readme.append(f"| {i} | {desc} |")

    from std import Solution  # type: ignore

    sol = Solution()
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        lines = raw.decode("utf-8").split("\n")
        assert len(lines) == 4, i
        load = eval(lines[0])
        runCost = int(lines[1])
        changeCost = int(lines[2])
        maxChanges = int(lines[3])
        got = sol.minComputeCost(load, runCost, changeCost, maxChanges)
        exp = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        assert got == exp, (i, got, exp)
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
    with open(DATA / "config.yaml", "w", encoding="utf-8", newline="\n") as f:
        f.write(config)
    with open(DATA / "README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(readme) + "\n")
    print("P5244 generated 10 cases OK")


def main() -> None:
    cases: List[Tuple[str, List[int], int, int, int]] = []

    cases.append(("样例1：满变更跟随 load", [1, 3, 2], 5, 2, 3))
    cases.append(("样例2：仅 1 次变更抬到峰值", [1, 3, 2], 5, 2, 1))
    cases.append(("样例3：恒定 load", [2, 2, 2], 3, 1, 1))

    cases.append(("边界：n=1", [0], 10, 10, 1))

    # hack：忽略 maxChanges 会选跟随序列；这里强制少变更
    cases.append(("hack：忽略变更上限会错", [1, 5, 1, 5, 1], 2, 10, 1))

    # 变更费很贵 → 尽量少变；运行费贵 → 尽量贴 load
    cases.append(("构造：变更费极高", [2, 4, 3], 1, 100, 2))
    cases.append(("构造：运行费极高贴 load", [1, 4, 2], 100, 1, 3))

    load8 = [RNG.randint(0, 15) for _ in range(20)]
    cases.append(("随机中：n=20", load8, RNG.randint(1, 20), RNG.randint(1, 20), RNG.randint(1, 8)))

    load9 = [RNG.randint(0, LOAD_MAX) for _ in range(N_MAX)]
    cases.append(("大数据：n=80 maxChanges=n", load9, 50, 50, N_MAX))

    load10 = [RNG.randint(0, LOAD_MAX) for _ in range(N_MAX)]
    cases.append(("大数据：n=80 紧变更上限", load10, COST_MAX, COST_MAX, 3))

    assert len(cases) == 10
    write_cases(cases)


if __name__ == "__main__":
    main()
