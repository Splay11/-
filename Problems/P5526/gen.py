# -*- coding: utf-8 -*-
"""生成 P5526 测试数据：样例在前，末两组近上限。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"
RNG = random.Random(5526)

CONFIG = """type: default
time: 2s
memory: 256m
subtasks:
  - score: 100
    type: sum
    cases:
{cases}
langs:
  - py.py3
  - java
  - cc.cc14o2
"""


def write_case(idx: int, content: str) -> None:
    text = content.rstrip("\n")
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))
    proc = subprocess.run(
        [sys.executable, str(STD)],
        input=text + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout.replace("\r\n", "\n")
    out = out.rstrip("\n") + "\n"
    (DATA / f"{idx}.out").write_bytes(out.encode("utf-8"))


def fmt(n: int, edges: list[tuple[int, int]]) -> str:
    lines = [f"{n} {len(edges)}"]
    lines += [f"{u} {v}" for u, v in edges]
    return "\n".join(lines)


def dag_chain(n: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(1, n)]


def cycle(n: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(1, n)] + [(n, 1)]


def random_dag(n: int, m: int) -> list[tuple[int, int]]:
    edges = set()
    while len(edges) < m:
        u = RNG.randint(1, n - 1)
        v = RNG.randint(u + 1, n)
        edges.add((u, v))
    return list(edges)


def random_with_cycle(n: int, m: int) -> list[tuple[int, int]]:
    edges = set(cycle(min(n, 5)))
    while len(edges) < m:
        u = RNG.randint(1, n)
        v = RNG.randint(1, n)
        edges.add((u, v))
    return list(edges)[:m]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    s1 = """5 6
2 4
1 2
3 4
1 5
4 5
3 5"""
    s2 = """5 8
2 1
1 5
4 3
5 4
4 5
5 3
3 2
1 3"""
    cases = [
        s1,
        s2,
        fmt(1, []),  # 单点无边
        fmt(1, [(1, 1)]),  # 自环
        fmt(3, [(1, 2), (2, 3)]),  # 链无环
        fmt(4, [(1, 2), (2, 3), (3, 1), (1, 4)]),  # 小环
        fmt(1000, dag_chain(1000)),
        fmt(2000, random_with_cycle(2000, 5000)),
        fmt(100000, dag_chain(100000) + [(100000, 1)]),  # 近上限有环
        fmt(100000, random_dag(100000, 200000)),  # 近上限无环
    ]
    assert len(cases) == 10
    for i, c in enumerate(cases, 1):
        write_case(i, c)

    case_lines = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    cfg = CONFIG.format(cases=case_lines)
    (ROOT / "config.yaml").write_text(cfg, encoding="utf-8")
    (DATA / "config.yaml").write_text(cfg, encoding="utf-8")
    print("P5526 gen done")


if __name__ == "__main__":
    main()
