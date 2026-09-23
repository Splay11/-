# -*- coding: utf-8 -*-
"""P5415 还原流量走法：10 组测例。

前 8 组小数据（样例、贪心死胡同、自环、重边、随机对拍）；
后 2 组 m=300，入口先走进高分支陷阱，卡回溯暴力。
"""
from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(541520260909)
START = "Core-SW-01"


def find_path(hops: list[tuple[str, str]]) -> list[str]:
    g: dict[str, list[str]] = defaultdict(list)
    for u, v in hops:
        g[u].append(v)
    for u in g:
        g[u].sort(reverse=True)
    route: list[str] = []
    stack = [START]
    while stack:
        u = stack[-1]
        vs = g.get(u)
        if vs:
            stack.append(vs.pop())
        else:
            route.append(u)
            stack.pop()
    route.reverse()
    return route


def brute_path(hops: list[tuple[str, str]]) -> list[str] | None:
    g: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for i, (u, v) in enumerate(hops):
        g[u].append((v, i))
    for u in g:
        g[u].sort()
    n = len(hops)
    used = [False] * n
    path = [START]
    found: list[str] = []

    def dfs(u: str, cnt: int) -> bool:
        if found:
            return True
        if cnt == n:
            found.extend(path)
            return True
        for v, i in g[u]:
            if used[i]:
                continue
            used[i] = True
            path.append(v)
            if dfs(v, cnt + 1):
                return True
            path.pop()
            used[i] = False
        return False

    dfs(START, 0)
    return found or None


def naive_greedy(hops: list[tuple[str, str]]) -> list[str] | None:
    g: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for i, (u, v) in enumerate(hops):
        g[u].append((v, i))
    for u in g:
        g[u].sort()
    used = [False] * len(hops)
    path = [START]
    u = START
    for _ in range(len(hops)):
        ok = False
        for v, i in g[u]:
            if used[i]:
                continue
            used[i] = True
            path.append(v)
            u = v
            ok = True
            break
        if not ok:
            return None
    if sum(used) != len(hops):
        return None
    return path


def walk_edges(rng: random.Random, start: str, nodes: list[str], n_edges: int):
    edges = []
    u = start
    for _ in range(n_edges):
        v = rng.choice(nodes)
        edges.append((u, v))
        u = v
    return edges, u


def make_trap(rng: random.Random, n_main: int, n_trap: int, n_main_nodes: int, n_trap_nodes: int):
    main_nodes = [START] + [f"B-{i}" for i in range(n_main_nodes)]
    trap_nodes = [f"A-{i}" for i in range(n_trap_nodes)]
    e1, pos = walk_edges(rng, START, main_nodes, n_main - 1)
    e1.append((pos, START))
    e2, _ = walk_edges(rng, "A-0", trap_nodes, n_trap)
    edges = e1 + [(START, "A-0")] + e2
    rng.shuffle(edges)
    return edges


def write_in(path: Path, hops: list[tuple[str, str]]) -> None:
    lines = [f"{u} {v}" for u, v in hops]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[str]) -> None:
    path.write_bytes((" ".join(ans) + "\n").encode("utf-8"))


def used_all(hops: list[tuple[str, str]], path: list[str]) -> bool:
    if len(path) != len(hops) + 1:
        return False
    from collections import Counter
    need = Counter(hops)
    got = Counter((path[i], path[i + 1]) for i in range(len(path) - 1))
    return need == got


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: list[list[tuple[str, str]]] = []

    # 1 样例1：两条合法走法，字典序取 R-A 开头
    cases.append(
        [
            ("Core-SW-01", "R-B"),
            ("Core-SW-01", "R-A"),
            ("R-A", "R-C"),
            ("R-C", "Core-SW-01"),
            ("R-B", "R-A"),
        ]
    )
    # 2 输入描述链
    cases.append(
        [
            ("N-A", "N-B"),
            ("Core-SW-01", "N-A"),
            ("Dev-P", "Dev-Q"),
            ("N-B", "Dev-P"),
        ]
    )
    # 3 纯贪心走进 A-1 死胡同
    cases.append(
        [
            ("Core-SW-01", "A-1"),
            ("Core-SW-01", "B-1"),
            ("B-1", "Core-SW-01"),
        ]
    )
    # 4 一条跳转
    cases.append([("Core-SW-01", "Z-9")])
    # 5 自环必须先走，不能先跳到更小的 A-1
    cases.append(
        [
            ("Core-SW-01", "Core-SW-01"),
            ("Core-SW-01", "A-1"),
        ]
    )
    # 6 多重边
    cases.append(
        [
            ("Core-SW-01", "M-2"),
            ("Core-SW-01", "M-2"),
            ("M-2", "Core-SW-01"),
            ("M-2", "T-1"),
        ]
    )
    # 7 小随机走
    e7, _ = walk_edges(RNG, START, [START, "P-1", "P-2", "Q-3"], 8)
    cases.append(e7)
    # 8 另一组构造
    e8, _ = walk_edges(RNG, START, [START, "K-1", "K-2", "K-3", "L-4"], 10)
    cases.append(e8)
    # 9-10 满规模陷阱
    cases.append(make_trap(RNG, 200, 99, 18, 12))
    cases.append(make_trap(RNG, 190, 109, 20, 14))

    assert len(cases) == 10
    for i, hops in enumerate(cases, 1):
        assert 1 <= len(hops) <= 300
        for u, v in hops:
            assert 1 <= len(u) <= 20 and 1 <= len(v) <= 20
            assert all(ch.isalnum() or ch == "-" for ch in u)
            assert all(ch.isalnum() or ch == "-" for ch in v)
        ans = find_path(hops)
        assert used_all(hops, ans), f"case {i} not euler"
        assert ans[0] == START
        if len(hops) <= 12:
            br = brute_path(hops)
            assert br == ans, f"case {i} brute mismatch {br} vs {ans}"
        if i == 3:
            assert naive_greedy(hops) is None
        if i == 5:
            greedy = naive_greedy(hops)
            assert greedy is None or greedy != ans
        write_in(DATA / f"{i}.in", hops)
        write_out(DATA / f"{i}.out", ans)
        got = find_path(
            [
                tuple(line.split())  # type: ignore
                for line in (DATA / f"{i}.in").read_text(encoding="utf-8").split("\n")
                if line.strip()
            ]
        )
        expect = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert expect.endswith("\n") and expect.count("\n") == 1
        raw_in = (DATA / f"{i}.in").read_bytes()
        assert not raw_in.endswith(b"\n")
        assert " ".join(got) + "\n" == expect, f"case {i} rewrite mismatch"

    print("ok", [len(c) for c in cases])


if __name__ == "__main__":
    main()
