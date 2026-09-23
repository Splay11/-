# -*- coding: utf-8 -*-
"""生成 P5257 data/*.in/*.out。.in 无行末多余换行；.out 恰一换行。"""

from __future__ import annotations

import random
from bisect import bisect_left
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 200000
W_MAX = 200000
SEED = 525720260816
RNG = random.Random(SEED)


class FenwickMax:
    def __init__(self, n: int):
        self.n = n
        self.a = [0] * (n + 1)

    def upd(self, i: int, v: int) -> None:
        while i <= self.n:
            if v > self.a[i]:
                self.a[i] = v
            i += i & -i

    def qry(self, i: int) -> int:
        r = 0
        while i > 0:
            if self.a[i] > r:
                r = self.a[i]
            i -= i & -i
        return r


def solve(n: int, edges: list[tuple[int, int, int]]) -> int:
    inc: list[list[int]] = [[] for _ in range(n + 1)]
    for _u, v, w in edges:
        inc[v].append(w)
    comp: list[list[int] | None] = [None] * (n + 1)
    bits: list[FenwickMax | None] = [None] * (n + 1)
    for i in range(1, n + 1):
        if inc[i]:
            comp[i] = sorted(set(inc[i]))
            bits[i] = FenwickMax(len(comp[i]))
    ans = 0
    for u, v, w in edges:
        best = 1
        if bits[u] is not None:
            k = bisect_left(comp[u], w)  # type: ignore[arg-type]
            if k:
                best = 1 + bits[u].qry(k)
        if best > ans:
            ans = best
        bits[v].upd(bisect_left(comp[v], w) + 1, best)  # type: ignore[arg-type, union-attr]
    return ans


def brute(n: int, edges: list[tuple[int, int, int]]) -> int:
    m = len(edges)
    dp = [1] * m
    for i in range(m):
        u, _v, w = edges[i]
        for j in range(i):
            _uj, vj, wj = edges[j]
            if vj == u and wj < w:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0


def fmt_in(n: int, edges: list[tuple[int, int, int]]) -> str:
    lines = [f"{n} {len(edges)}"]
    lines.extend(f"{u} {v} {w}" for u, v, w in edges)
    return "\n".join(lines)


def write_pair(idx: int, n: int, edges: list[tuple[int, int, int]]) -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    m = len(edges)
    assert 1 <= n <= N_MAX and 1 <= m <= N_MAX
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and 0 <= w <= W_MAX
    ans = solve(n, edges)
    if m <= 400:
        b = brute(n, edges)
        if b != ans:
            raise RuntimeError(f"case {idx}: brute {b} != {ans}")
    tin = fmt_in(n, edges)
    tout = f"{ans}\n"
    if tin.endswith("\n"):
        raise RuntimeError(f"case {idx}: .in ends with newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"case {idx}: bad .out newline")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))
    return ans


def rand_small(n: int, m: int) -> list[tuple[int, int, int]]:
    edges = []
    for _ in range(m):
        u = RNG.randint(1, n)
        v = RNG.randint(1, n)
        w = RNG.randint(0, 40)
        edges.append((u, v, w))
    return edges


def main() -> None:
    cases: list[tuple[int, list[tuple[int, int, int]]]] = []

    # 1-2 改写样例
    cases.append((2, [(1, 2, 4), (2, 1, 5), (1, 2, 6)]))
    cases.append((4, [(2, 1, 3), (1, 3, 1), (3, 4, 2), (4, 2, 4)]))

    # 3 原样例：卡忽略下标去走环
    cases.append((3, [(3, 1, 3), (1, 2, 1), (2, 3, 2)]))

    # 4 边界：单点自环
    cases.append((1, [(1, 1, 0)]))

    # 5 hack：分值全相同，只能 1
    cases.append((3, [(1, 2, 5), (2, 3, 5), (3, 1, 5)]))

    # 6 hack：自环分值递增
    cases.append((1, [(1, 1, 1), (1, 1, 2), (1, 1, 3)]))

    # 7 构造：更长链末分值更大，盖住可延伸的短链
    # 1->2 w=10 长度1；1->2 w=1 后接 2->3 w=2，正解为 2
    cases.append((3, [(1, 2, 10), (1, 2, 1), (2, 3, 2)]))

    # 8 随机小数据
    cases.append((12, rand_small(12, 80)))

    # 9 压力：沿环走满，答案 = m
    n9 = N_MAX
    m9 = N_MAX
    e9 = [((i % n9) + 1, ((i + 1) % n9) + 1, i) for i in range(m9)]
    cases.append((n9, e9))

    # 10 压力：随机大图
    n10 = N_MAX
    m10 = N_MAX
    e10 = rand_small(n10, m10)
    # rand_small 用了 w<=40，大图改到满值域
    e10 = [
        (RNG.randint(1, n10), RNG.randint(1, n10), RNG.randint(0, W_MAX))
        for _ in range(m10)
    ]
    cases.append((n10, e10))

    assert len(cases) == 10
    for i, (n, edges) in enumerate(cases, 1):
        ans = write_pair(i, n, edges)
        print(f"{i}.in n={n} m={len(edges)} ans={ans}")


if __name__ == "__main__":
    main()
