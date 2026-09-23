# -*- coding: utf-8 -*-
"""P7008 测试数据。约束对齐题面_改写.md：m<=250000，节点总数<=250000，1<=v<=1e9。"""

from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DATA = ROOT / "data"
SEED = 700820260818
RNG = random.Random(SEED)

M_MAX = 250000
N_MAX = 250000
V_MAX = 10**9


def merge_rev(lists: list[list[int]]) -> list[int]:
    out: list[int] = []
    for lst in reversed(lists):
        out.extend(lst)
    return out


def fmt_in(lists: list[list[int]]) -> str:
    parts = []
    for lst in lists:
        if not lst:
            parts.append("{}")
        else:
            parts.append("{" + ",".join(str(x) for x in lst) + "}")
    return "[" + ",".join(parts) + "]"


def fmt_out(vals: list[int]) -> str:
    if not vals:
        return "{}\n"
    return "{" + ",".join(str(x) for x in vals) + "}\n"


def total_nodes(lists: list[list[int]]) -> int:
    return sum(len(x) for x in lists)


def validate(lists: list[list[int]]) -> None:
    assert 1 <= len(lists) <= M_MAX
    assert total_nodes(lists) <= N_MAX
    for lst in lists:
        assert all(1 <= x <= V_MAX for x in lst)


def write_pair(idx: int, lists: list[list[int]]) -> None:
    from std import format_list, merge_rev as mr
    from std import parse_lists

    DATA.mkdir(parents=True, exist_ok=True)
    validate(lists)
    tin = fmt_in(lists)
    tout = fmt_out(merge_rev(lists))
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in 末尾有换行")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out 换行不合法")
    got = format_list(mr(parse_lists(tin))) + "\n"
    if got != tout:
        raise RuntimeError(f"{idx}: std 与 gen 不一致")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))


def rand_list(n: int, vmax: int = 100) -> list[int]:
    return [RNG.randint(1, vmax) for _ in range(n)]


def main() -> None:
    groups: list[list[list[int]]] = []
    groups.append([[4, 5], [9], [1, 1, 2]])
    groups.append([[8], [], [2, 2]])
    groups.append([[7, 8, 9]])
    groups.append([[], [], []])
    groups.append([[1], [2], [3]])
    groups.append([[1, 2], [3, 4]])
    groups.append([[], [10], [], [20, 21], []])
    groups.append(
        [rand_list(RNG.randint(0, 5), 20) for _ in range(8)] + [[V_MAX], [1, 1, 1]]
    )

    m9 = 20000
    g9: list[list[int]] = []
    left = 80000
    for _ in range(m9):
        if left <= 0:
            g9.append([])
            continue
        n = min(RNG.randint(0, 6), left)
        g9.append(rand_list(n, 10**6) if n else [])
        left -= n
    groups.append(g9)

    long_n = 200000
    singles = 20000
    empties = 30000
    g10: list[list[int]] = []
    g10.extend([[] for _ in range(empties)])
    g10.append([RNG.randint(1, V_MAX) for _ in range(long_n)])
    g10.extend([[RNG.randint(1, 1000)] for _ in range(singles)])
    assert total_nodes(g10) == long_n + singles
    assert len(g10) == empties + 1 + singles
    groups.append(g10)

    assert len(groups) == 10
    for i, lists in enumerate(groups, 1):
        write_pair(i, lists)
        print(f"{i}.in m={len(lists)} nodes={total_nodes(lists)}")


if __name__ == "__main__":
    main()
