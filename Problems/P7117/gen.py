# -*- coding: utf-8 -*-
"""P7117 造数：中心出发的格子 TSP。"""
from __future__ import annotations

import importlib.util
from itertools import permutations
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7117)


def load_std():
    spec = importlib.util.spec_from_file_location("p7117_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.min_steps


min_steps = load_std()


def zeros(n, m):
    return [[0] * m for _ in range(n)]


def count_ones(g):
    return sum(v != 0 for row in g for v in row)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def points_of(g):
    n, m = len(g), len(g[0])
    sr, sc = n // 2, m // 2
    pts = [(sr, sc)]
    for i in range(n):
        for j in range(m):
            if g[i][j] != 0 and (i != sr or j != sc):
                pts.append((i, j))
    return pts


def nearest_neighbor(g):
    """每次走向最近未访问必访点，最后回中心。"""
    pts = points_of(g)
    if len(pts) == 1:
        return 0
    used = [False] * len(pts)
    used[0] = True
    cur = 0
    cost = 0
    for _ in range(len(pts) - 1):
        best = -1
        best_d = 10**9
        for j in range(1, len(pts)):
            if used[j]:
                continue
            d = manhattan(pts[cur], pts[j])
            if d < best_d:
                best_d = d
                best = j
        used[best] = True
        cost += best_d
        cur = best
    return cost + manhattan(pts[cur], pts[0])


def brute(g):
    pts = points_of(g)
    if len(pts) <= 1:
        return 0
    extra = list(range(1, len(pts)))
    best = 10**9
    for order in permutations(extra):
        cost = 0
        cur = 0
        for j in order:
            cost += manhattan(pts[cur], pts[j])
            cur = j
        cost += manhattan(pts[cur], pts[0])
        if cost < best:
            best = cost
    return best


def place_ones(n, m, coords, center_one=False):
    g = zeros(n, m)
    if center_one:
        g[n // 2][m // 2] = 1
    for r, c in coords:
        g[r][c] = 1
    return g


def random_grid(n, m, k, include_center):
    g = zeros(n, m)
    cells = [(i, j) for i in range(n) for j in range(m)]
    if include_center:
        g[n // 2][m // 2] = 1
        cells.remove((n // 2, m // 2))
        k -= 1
    k = max(0, min(k, len(cells)))
    RNG.shuffle(cells)
    for i in range(k):
        r, c = cells[i]
        g[r][c] = 1
    return g


def write_case(idx, g):
    n, m = len(g), len(g[0])
    assert n % 2 == 1 and m % 2 == 1
    assert 1 <= n <= 21 and 1 <= m <= 21
    ones = count_ones(g)
    assert ones <= 15
    assert all(v in (0, 1) for row in g for v in row)
    lines = [f"{n} {m}"]
    for row in g:
        lines.append(" ".join(str(x) for x in row))
    (DATA / f"{idx}.in").write_bytes("\n".join(lines).encode("utf-8"))
    ans = min_steps(g)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例
    cases.append([[1, 0, 0], [0, 1, 0], [1, 0, 0]])
    # 2. 1x1
    cases.append([[1]])
    # 3. 全 0
    cases.append(zeros(3, 3))
    # 4. 只有中心是 1
    g = zeros(5, 5)
    g[2][2] = 1
    cases.append(g)
    # 5. 中心为 0，两角必访
    cases.append(place_ones(3, 3, [(0, 0), (0, 2)]))
    # 6. 小随机，可与全排列对拍
    cases.append(random_grid(5, 5, 5, True))
    # 7. 构造：三方向拉开，卡最近邻
    cases.append(place_ones(5, 5, [(0, 0), (0, 4), (4, 0)], center_one=True))
    # 8. 一行上的若干 1
    g = zeros(1, 11)
    for j in range(0, 11, 2):
        g[0][j] = 1
    cases.append(g)
    # 9. 大数据随机
    cases.append(random_grid(21, 21, 12, True))
    # 10. 大数据拉满 15 个 1
    cases.append(random_grid(21, 21, 15, False))

    notes = [
        "样例 3x3，答案 6",
        "n=m=1",
        "全 0，答案 0",
        "只有中心非 0，答案 0",
        "中心为 0，访问两角再回来",
        "5x5 随机 5 个 1，与暴力对拍",
        "三方向拉开，卡最近邻",
        "1x11 隔点为 1",
        "21x21、12 个 1 压测",
        "21x21、15 个 1 压测",
    ]

    for i, g in enumerate(cases, 1):
        ans = write_case(i, g)
        nn = nearest_neighbor(g)
        extra = ""
        pts = points_of(g)
        if len(pts) <= 8:
            b = brute(g)
            if b != ans:
                raise SystemExit(f"DP 与暴力不一致：第 {i} 组 {ans} vs {b}")
            extra = f" brute={b}"
        print(f"case {i}: {len(g)}x{len(g[0])} ones={count_ones(g)} k={len(pts)} ans={ans} nn={nn}{extra} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        n, m = map(int, lines[0].split())
        g = [list(map(int, lines[r + 1].split())) for r in range(n)]
        got = min_steps(g)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out")
        if (DATA / f"{i}.in").read_bytes().endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    # 至少一组卡住最近邻
    hacked = False
    for idx in range(1, 11):
        raw = (DATA / f"{idx}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        n, m = map(int, lines[0].split())
        g = [list(map(int, lines[r + 1].split())) for r in range(n)]
        if nearest_neighbor(g) != min_steps(g):
            hacked = True
            break
    if not hacked:
        raise SystemExit("没有任何一组能卡掉最近邻贪心")

    print("gen ok")


if __name__ == "__main__":
    main()
