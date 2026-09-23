# -*- coding: utf-8 -*-
"""P7003 造数：更新任务最早完工（DAG 最长路）。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(7003)


def min_finish(n: int, prev: List[int], next_arr: List[int], time: List[int]) -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.Solution().minFinishTime(n, prev, next_arr, time)


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 40:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, n: int, prev: List[int], next_arr: List[int], time: List[int]) -> None:
    assert 1 <= n <= 10**4
    assert len(prev) == len(next_arr) <= 2 * 10**4
    assert len(time) == n
    for u, v in zip(prev, next_arr):
        assert 0 <= u < n and 0 <= v < n
    for t in time:
        assert 1 <= t <= 10**4
    text_in = "\n".join([str(n), fmt_arr(prev), fmt_arr(next_arr), fmt_arr(time)])
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    ans = min_finish(n, prev, next_arr, time)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")


def chain_dag(n: int) -> Tuple[List[int], List[int], List[int]]:
    prev = list(range(n - 1))
    nxt = list(range(1, n))
    time = [RNG.randint(1, 10) for _ in range(n)]
    return prev, nxt, time


def random_dag(n: int, m: int) -> Tuple[List[int], List[int], List[int]]:
    # 只连 i -> j (i < j) 保证无环
    edges = set()
    while len(edges) < m and m > 0:
        a = RNG.randint(0, n - 2)
        b = RNG.randint(a + 1, n - 1)
        edges.add((a, b))
    prev = [e[0] for e in edges]
    nxt = [e[1] for e in edges]
    time = [RNG.randint(1, 100) for _ in range(n)]
    return prev, nxt, time


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    cases = []

    # 1-3 样例
    cases.append((1, [], [], [5]))
    cases.append((3, [0, 1], [2, 2], [3, 2, 5]))
    cases.append((4, [0, 0, 1, 2], [1, 2, 3, 3], [1, 2, 3, 4]))

    # 4: 自环 → -1
    cases.append((2, [0], [0], [1, 1]))

    # 5: 简单环 → -1
    cases.append((3, [0, 1, 2], [1, 2, 0], [1, 1, 1]))

    # 6: 无边，并行 → max(time)
    cases.append((4, [], [], [2, 9, 3, 4]))

    # 7: 链
    p, nx, t = chain_dag(8)
    cases.append((8, p, nx, t))

    # 8: 中等随机 DAG
    p, nx, t = random_dag(50, 80)
    cases.append((50, p, nx, t))

    # 9: 大 DAG
    p, nx, t = random_dag(5000, 8000)
    cases.append((5000, p, nx, t))

    # 10: 接近上限 + 重边
    n = 10000
    prev = []
    nxt = []
    for i in range(min(19998, n - 1)):
        prev.append(i % (n - 1))
        nxt.append((i % (n - 1)) + 1)
    # 加几条重边
    prev += [0, 0]
    nxt += [1, 1]
    time = [1] * n
    cases.append((n, prev[:20000], nxt[:20000], time))

    assert len(cases) == 10
    assert min_finish(*cases[0]) == 5
    assert min_finish(*cases[1]) == 8
    assert min_finish(*cases[2]) == 8
    assert min_finish(*cases[3]) == -1
    assert min_finish(*cases[4]) == -1
    assert min_finish(*cases[5]) == 9

    for i, c in enumerate(cases, 1):
        write_case(i, *c)
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
        "主造数脚本：题目根目录 `gen.py`。stdin 四行：n / prev / next / time。\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    print("P7003 data ok:", [min_finish(*c) for c in cases[:6]])


if __name__ == "__main__":
    main()
