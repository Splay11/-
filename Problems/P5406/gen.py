# -*- coding: utf-8 -*-
"""P5406 应急协议：至多免费走一条通道。"""
from __future__ import annotations

import heapq
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_with_one_free, dijkstra  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(540620260912)
INF = 10 ** 18


def make_adj(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def brute(n, s, t, edges):
    if s == t:
        return 0
    adj0 = make_adj(n, edges)
    ans = dijkstra(n, s, adj0)[t]
    for i in range(len(edges)):
        u, v, w = edges[i]
        tmp = list(edges)
        tmp[i] = (u, v, 0)
        adj = make_adj(n, tmp)
        d = dijkstra(n, s, adj)[t]
        if d < ans:
            ans = d
    return -1 if ans >= INF else ans


def tree(n, wmin=1, wmax=10):
    edges = []
    for i in range(2, n + 1):
        p = RNG.randint(1, i - 1)
        edges.append((p, i, RNG.randint(wmin, wmax)))
    return edges


def extra(n, cnt, wmin=1, wmax=20):
    edges = []
    for _ in range(cnt):
        u = RNG.randint(1, n)
        v = RNG.randint(1, n)
        edges.append((u, v, RNG.randint(wmin, wmax)))
    return edges


def write_case(idx, n, s, t, edges, check=False):
    adj = make_adj(n, edges)
    ans = min_with_one_free(n, s, t, edges, adj)
    if check:
        bv = brute(n, s, t, edges)
        if bv != ans:
            raise RuntimeError(f"case {idx} brute {bv} vs std {ans}")
    lines = [f"{n} {len(edges)} {s} {t}"]
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    (DATA / f"{idx}.in").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (DATA / f"{idx}.out").write_text(str(ans) + "\n", encoding="utf-8")
    print(f"wrote {idx}.in n={n} m={len(edges)} ans={ans}")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    write_case(1, 4, 1, 4, [(1, 2, 5), (2, 4, 5), (1, 3, 100), (3, 4, 1)], check=True)
    write_case(2, 3, 1, 3, [(1, 2, 5)], check=True)
    write_case(3, 5, 2, 2, [(1, 2, 3), (2, 3, 4), (4, 5, 9)], check=True)
    write_case(4, 3, 1, 3, [(1, 2, 1), (2, 3, 1), (1, 3, 100)], check=True)
    write_case(5, 2, 1, 2, [(1, 2, 9)], check=True)
    write_case(6, 30, 1, 30, tree(30, 1, 20) + extra(30, 15, 1, 50), check=True)
    write_case(7, 800, 1, 800, tree(800, 1, 100) + extra(800, 400, 1, 1000))
    chain = [(i, i + 1, 100) for i in range(1, 8000)]
    write_case(8, 8000, 1, 8000, chain)
    write_case(9, 8000, 1, 8000, tree(8000, 1, 10 ** 6) + extra(8000, 12000, 1, 10 ** 6))
    e10 = [(i, i + 1, 10 ** 6) for i in range(1, 8000)] + [(1, 4000, 10 ** 6), (4000, 8000, 1)]
    write_case(10, 8000, 1, 8000, e10)


if __name__ == "__main__":
    main()
