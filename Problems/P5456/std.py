# 关键点最短路 + 枚举接人子集 + TSP 状压，再与步行时间取最大值

import heapq

INF = 10 ** 18


def dijkstra(p, adj, src):
    # 从 src 出发的最短公里数
    dist = [INF] * (p + 1)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def min_meet_time(p, edges, a, b, friends):
    """
    小红从 a 驾车，馆子在 b，friends 是同伴所在路口。
    驾车每公里 2 分钟，步行每公里 10 分钟。
    返回所有人到达的最短汇合时间。
    """
    adj = [[] for _ in range(p + 1)]
    for x, y, c, z in edges:
        adj[x].append((y, c))
        if z == 1:
            adj[y].append((x, c))
    q = len(friends)
    # 只对出发、馆子、同伴这些关键点跑最短路
    sources = [a, b] + friends
    sp = {}
    seen = set()
    for s in sources:
        if s in seen:
            continue
        seen.add(s)
        sp[s] = dijkstra(p, adj, s)

    def dist(u, v):
        return sp[u][v]

    walk = [10 * dist(f, b) for f in friends]
    if q == 0:
        return 2 * dist(a, b)

    # dp[mask][i]：已接 mask 里的同伴，当前停在同伴 i 处的最短驾车公里
    dp = [[INF] * q for _ in range(1 << q)]
    for i in range(q):
        dp[1 << i][i] = dist(a, friends[i])
    for mask in range(1 << q):
        for i in range(q):
            if dp[mask][i] >= INF:
                continue
            if (mask >> i) & 1 == 0:
                continue
            for j in range(q):
                if (mask >> j) & 1:
                    continue
                nmask = mask | (1 << j)
                nd = dp[mask][i] + dist(friends[i], friends[j])
                if nd < dp[nmask][j]:
                    dp[nmask][j] = nd

    ans = INF
    for mask in range(1 << q):
        if mask == 0:
            car = 2 * dist(a, b)
        else:
            car = INF
            for i in range(q):
                if (mask >> i) & 1:
                    car = min(car, 2 * (dp[mask][i] + dist(friends[i], b)))
        walkers = 0
        for i in range(q):
            if (mask >> i) & 1 == 0:
                walkers = max(walkers, walk[i])
        cur = car if car > walkers else walkers
        if cur < ans:
            ans = cur
    return ans


def main():
    p, e, a, b = map(int, input().split())
    edges = []
    for _ in range(e):
        x, y, c, z = map(int, input().split())
        edges.append((x, y, c, z))
    q = int(input())
    if q == 0:
        friends = []
    else:
        friends = list(map(int, input().split()))
    print(min_meet_time(p, edges, a, b, friends))


if __name__ == "__main__":
    main()
