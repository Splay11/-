# -*- coding: utf-8 -*-
"""P5329 造数：油箱状态最短路。"""
import heapq
import os
import random

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(k, q, r, edges):
    g = [[] for _ in range(k + 1)]
    for a, b, c, t in edges:
        g[a].append((b, c, t))
        g[b].append((a, c, t))
    inf = 10 ** 18
    dist = [[inf] * (q + 1) for _ in range(k + 1)]
    dist[1][q] = 0
    h = [(0, 1, q)]
    while h:
        tm, u, f = heapq.heappop(h)
        if tm != dist[u][f]:
            continue
        if f < q:
            nf = f + 1
            ntm = tm + r[u - 1]
            if ntm < dist[u][nf]:
                dist[u][nf] = ntm
                heapq.heappush(h, (ntm, u, nf))
        for v, c, t in g[u]:
            if f >= c:
                nf = f - c
                ntm = tm + t
                if ntm < dist[v][nf]:
                    dist[v][nf] = ntm
                    heapq.heappush(h, (ntm, v, nf))
    ans = min(dist[k])
    return -1 if ans >= inf else ans


def write_file(idx, k, q, r, edges):
    e = len(edges)
    assert 2 <= k <= 1000
    assert 1 <= e <= 10000
    assert 1 <= q <= 100
    assert len(r) == k
    lines = ["%d %d %d" % (k, e, q), " ".join(str(x) for x in r)]
    for a, b, c, t in edges:
        lines.append("%d %d %d %d" % (a, b, c, t))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(str(solve(k, q, r, edges)) + "\n")


def main():
    rng = random.Random(5329)
    write_file(1, 3, 4, [4, 1, 9], [(1, 2, 2, 3), (2, 3, 2, 4)])
    write_file(2, 2, 3, [2, 8], [(1, 2, 5, 4)])
    write_file(3, 2, 3, [5, 1], [(1, 2, 2, 8)])
    write_file(4, 3, 3, [2, 3, 5], [(1, 2, 1, 10), (1, 3, 1, 100), (2, 3, 3, 1)])
    write_file(5, 4, 5, [1, 2, 3, 4], [(1, 2, 2, 5), (2, 3, 2, 6), (3, 4, 2, 7)])
    # 6 免费补油
    write_file(6, 3, 2, [0, 0, 0], [(1, 2, 2, 4), (2, 3, 2, 5)])
    # 7 随机中等
    k, q = 20, 20
    r = [rng.randint(0, 10) for _ in range(k)]
    edges = []
    for i in range(1, k):
        edges.append((i, i + 1, rng.randint(1, 5), rng.randint(1, 20)))
    for _ in range(15):
        a, b = rng.randint(1, k), rng.randint(1, k)
        if a != b:
            edges.append((a, b, rng.randint(1, 8), rng.randint(1, 30)))
    write_file(7, k, q, r, edges)
    # 8 稍大
    k, q = 80, 30
    r = [rng.randint(1, 20) for _ in range(k)]
    edges = []
    for i in range(1, k):
        edges.append((i, i + 1, rng.randint(1, 6), rng.randint(1, 50)))
    for _ in range(40):
        a, b = rng.randint(1, k), rng.randint(1, k)
        if a != b:
            edges.append((a, b, rng.randint(1, 10), rng.randint(1, 80)))
    write_file(8, k, q, r, edges)
    # 9 大数据
    k, q = 400, 60
    r = [rng.randint(0, 40) for _ in range(k)]
    edges = []
    for i in range(1, k):
        edges.append((i, i + 1, rng.randint(1, 8), rng.randint(1, 100)))
    for _ in range(800):
        a, b = rng.randint(1, k), rng.randint(1, k)
        if a != b:
            edges.append((a, b, rng.randint(1, 20), rng.randint(1, 200)))
    write_file(9, k, q, r, edges)
    # 10 上限附近
    k, q = 1000, 100
    r = [rng.randint(0, 100) for _ in range(k)]
    edges = []
    for i in range(1, k):
        edges.append((i, i + 1, rng.randint(1, 10), rng.randint(1, 200)))
    for _ in range(3000):
        a, b = rng.randint(1, k), rng.randint(1, k)
        if a != b:
            edges.append((a, b, rng.randint(1, 40), rng.randint(1, 1000)))
    write_file(10, k, q, r, edges)


if __name__ == "__main__":
    main()
