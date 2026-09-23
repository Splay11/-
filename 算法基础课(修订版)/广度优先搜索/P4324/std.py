# -*- coding: utf-8 -*-
import sys
from collections import deque

def build_graph(n, m, lines):
    """构建：站点->线路、线路图邻接表"""
    station_lines = [[] for _ in range(n)]
    for li, stations in enumerate(lines):
        for s in stations:
            station_lines[s].append(li)

    adj = [set() for _ in range(m)]
    # 同一站点上的所有线路两两连边
    for s in range(n):
        lst = station_lines[s]
        L = len(lst)
        for i in range(L):
            a = lst[i]
            for j in range(i + 1, L):
                b = lst[j]
                adj[a].add(b)
                adj[b].add(a)
    # 转为列表，便于遍历
    adj = [list(nei) for nei in adj]
    return station_lines, adj

def min_transfers_for_query(s, t, station_lines, adj):
    """在线路图上求最少换乘次数"""
    if s == t:
        return 0
    starts = station_lines[s]
    targets = set(station_lines[t])
    if not starts or not targets:
        return -1
    # 若有一条线路同时包含 s 与 t，换乘为 0
    for x in starts:
        if x in targets:
            return 0

    m = len(adj)
    dist = [-1] * m
    q = deque()
    for x in starts:
        dist[x] = 0
        q.append(x)

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1  # 换乘一次
                if v in targets:
                    return dist[v]
                q.append(v)
    return -1  # 不可达

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    n, m, k = next(it), next(it), next(it)  # 站点数、线路数、查询数

    lines = []
    for _ in range(m):
        cnt = next(it)              # 本线路站点数量
        stations = [next(it) for _ in range(cnt)]
        lines.append(stations)

    station_lines, adj = build_graph(n, m, lines)

    out = []
    for _ in range(k):
        s, t = next(it), next(it)
        out.append(str(min_transfers_for_query(s, t, station_lines, adj)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
