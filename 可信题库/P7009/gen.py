# -*- coding: utf-8 -*-
"""P7009 造数：带风险额度的最短路。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7009)
COMPILE_SH = Path(r"d:\机考出题\problem-maker\compile.sh")


def solve(n: int, edges: List[List[int]], src: int, dst: int, budget: int) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.Solution().minTrustDelay(n, edges, src, dst, budget)


def fmt_edges(edges: List[List[int]]) -> str:
    if len(edges) <= 30:
        inner = ", ".join("[" + ", ".join(str(x) for x in e) + "]" for e in edges)
        return "[" + inner + "]"
    return json.dumps(edges, separators=(",", ":"))


def write_case(idx: int, n: int, edges: List[List[int]], src: int, dst: int, budget: int) -> None:
    assert 1 <= n <= 200
    assert 0 <= len(edges) <= 4000
    for u, v, d, r in edges:
        assert 0 <= u < n and 0 <= v < n
        assert 1 <= d <= 1000
        assert 0 <= r <= 1000
    assert 0 <= src < n and 0 <= dst < n
    assert 0 <= budget <= 1000
    text_in = "\n".join([str(n), fmt_edges(edges), str(src), str(dst), str(budget)])
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    ans = solve(n, edges, src, dst, budget)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")


def rand_graph(n: int, m: int, delay_hi: int, risk_hi: int) -> List[List[int]]:
    edges = []
    for _ in range(m):
        u = RNG.randint(0, n - 1)
        v = RNG.randint(0, n - 1)
        d = RNG.randint(1, delay_hi)
        r = RNG.randint(0, risk_hi)
        edges.append([u, v, d, r])
    return edges


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    Case = Tuple[int, List[List[int]], int, int, int]
    cases: List[Case] = []

    # 1-3 样例
    e123 = [[0, 1, 5, 3], [1, 2, 4, 2], [0, 2, 20, 1]]
    cases.append((3, e123, 0, 2, 5))
    cases.append((3, e123, 0, 2, 4))
    cases.append((4, [[0, 1, 1, 8], [0, 2, 5, 1], [2, 1, 1, 1], [1, 3, 1, 3]], 0, 3, 5))

    # 4 src==dst
    cases.append((1, [], 0, 0, 0))

    # 5 不可达 / 额度 0 只能走 risk=0
    cases.append((3, [[0, 1, 1, 0], [1, 2, 2, 1]], 0, 2, 0))

    # 6 重边自环；短高风险 vs 长低风险
    cases.append((3, [[0, 1, 1, 10], [0, 1, 8, 1], [1, 1, 1, 0], [1, 2, 1, 1]], 0, 2, 2))

    # 7 中等随机
    cases.append((20, rand_graph(20, 80, 20, 20), 0, 19, 40))

    # 8 hack：只按节点最短时延会错
    cases.append(
        (
            5,
            [
                [0, 1, 1, 9],
                [0, 2, 10, 1],
                [2, 1, 1, 1],
                [1, 3, 1, 5],
                [3, 4, 1, 0],
                [0, 4, 100, 0],
            ],
            0,
            4,
            8,
        )
    )

    # 9 较大
    cases.append((80, rand_graph(80, 800, 50, 30), 0, 79, 200))

    # 10 极限
    cases.append((200, rand_graph(200, 4000, 1000, 1000), 0, 199, 1000))

    assert len(cases) == 10
    assert solve(*cases[0]) == 9
    assert solve(*cases[1]) == 20
    assert solve(*cases[2]) == 7
    assert solve(*cases[3]) == 0

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
        "主造数脚本：题目根目录 `gen.py`。stdin 五行：n、edges、src、dst、riskBudget。\n"
        "1-3 样例；4 起点即终点；5 额度卡死；6 重边；8 卡「每点只留最小时延」；9-10 压力。\n",
        encoding="utf-8",
    )
    shutil.copyfile(COMPILE_SH, DATA / "compile.sh")
    print("P7009 data ok")


if __name__ == "__main__":
    main()
