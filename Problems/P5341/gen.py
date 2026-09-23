# -*- coding: utf-8 -*-
"""P5341 造数：恰好升级 t 条边后的最大瓶颈带宽。"""
from __future__ import annotations

import importlib.util
from collections import deque
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5341)


def load_std():
    spec = importlib.util.spec_from_file_location("p5341_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.max_bottleneck


max_bottleneck = load_std()


def solve_atmost(c, t, edges):
    """错误：把「恰好 t 次」当成「最多 t 次」。"""

    def ok(x):
        g = [[] for _ in range(c)]
        for a, b, w in edges:
            if 2 * w < x:
                continue
            need = 1 if w < x else 0
            g[a].append((b, need))
            g[b].append((a, need))
        dist = [10**9] * c
        q = deque([0])
        dist[0] = 0
        while q:
            u = q.popleft()
            for v, need in g[u]:
                nd = dist[u] + need
                if nd < dist[v]:
                    dist[v] = nd
                    q.append(v)
        return dist[c - 1] <= t

    ans = -1
    for x in range(1, 1999):
        if ok(x):
            ans = x
    return ans


def write_case(idx, c, t, edges):
    d = len(edges)
    assert 2 <= c <= 100
    assert 1 <= d <= 1000
    assert 0 <= t <= min(10, d)
    for x, y, b in edges:
        assert 0 <= x < c and 0 <= y < c and x != y
        assert 1 <= b <= 999
    ans = max_bottleneck(c, t, edges)
    lines = [f"{c} {d} {t}"]
    for x, y, b in edges:
        lines.append(f"{x} {y} {b}")
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_connected(c, d, t, lo=1, hi=999):
    edges = []
    seen = set()

    def add(u, v, b):
        a, e = (u, v) if u < v else (v, u)
        if a == e or (a, e) in seen:
            return False
        seen.add((a, e))
        edges.append((u, v, b))
        return True

    for i in range(1, c):
        p = RNG.randint(0, i - 1)
        add(p, i, RNG.randint(lo, hi))
    while len(edges) < d:
        u = RNG.randint(0, c - 1)
        v = RNG.randint(0, c - 1)
        add(u, v, RNG.randint(lo, hi))
    return c, t, edges


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例1：不连通
    cases.append((3, 0, [(0, 1, 7)]))
    # 2. 样例2
    cases.append(
        (
            5,
            2,
            [
                (0, 1, 11),
                (0, 2, 16),
                (1, 2, 4),
                (1, 3, 22),
                (2, 4, 14),
                (3, 4, 19),
            ],
        )
    )
    # 3. 样例3：卡「最多 t 次」
    cases.append(
        (
            6,
            2,
            [
                (0, 1, 9),
                (1, 5, 9),
                (0, 2, 14),
                (2, 3, 14),
                (3, 5, 14),
                (0, 5, 36),
                (2, 4, 7),
                (4, 5, 7),
            ],
        )
    )
    # 4. 两个点，不升级
    cases.append((2, 0, [(0, 1, 40)]))
    # 5. 两个点，必须升级 1 次
    cases.append((2, 1, [(0, 1, 40)]))
    # 6. 链，k=0，卡成只看最大边
    cases.append((4, 0, [(0, 1, 100), (1, 2, 3), (2, 3, 100)]))
    # 7. 奇数长度链，恰好升级才能抬瓶颈
    cases.append((4, 1, [(0, 1, 12), (1, 2, 12), (2, 3, 5)]))
    # 8. 带宽上界 999
    cases.append((3, 1, [(0, 1, 999), (1, 2, 999)]))
    # 9. 接近上限的随机连通图
    cases.append(rand_connected(80, 400, 5))
    # 10. 满约束
    cases.append(rand_connected(100, 1000, 10))

    notes = [
        "样例1 不连通",
        "样例2 升级两条边得到 28",
        "样例3 直连不能恰好升 2 次，卡最多 t 次假解",
        "n=2 且 t=0，答案为原带宽",
        "n=2 且 t=1，答案为 2 倍带宽",
        "k=0 瓶颈是链上最小值",
        "长度为 3 的链，恰好升 1 次",
        "带宽取到 999",
        "n=80 随机连通",
        "n=100 m=1000 t=10",
    ]

    for i, (c, t, edges) in enumerate(cases, 1):
        ans = write_case(i, c, t, edges)
        am = solve_atmost(c, t, edges)
        print(f"case {i}: c={c} d={len(edges)} t={t} ans={ans} atmost={am} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        c, d, t = map(int, lines[0].split())
        edges = []
        for j in range(1, d + 1):
            x, y, b = map(int, lines[j].split())
            edges.append((x, y, b))
        got = max_bottleneck(c, t, edges)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    c, t, edges = cases[2]
    if solve_atmost(c, t, edges) == max_bottleneck(c, t, edges):
        raise SystemExit("第 3 组未能卡掉「最多 t 次」假解")
    if max_bottleneck(2, 0, [(0, 1, 40)]) != 40:
        raise SystemExit("第 4 组答案错误")
    if max_bottleneck(2, 1, [(0, 1, 40)]) != 80:
        raise SystemExit("第 5 组答案错误")

    print("gen ok")


if __name__ == "__main__":
    main()
