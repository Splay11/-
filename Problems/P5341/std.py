import heapq


def max_bottleneck(c, t, edges):
    graph = [[] for _ in range(c)]
    for x, y, b in edges:
        graph[x].append((y, b))
        graph[y].append((x, b))
    # 起点还没有走过任何边，瓶颈视为正无穷
    INF = 10 ** 9
    # f[u][used]：到达 u、恰好升级 used 次时，能得到的最大瓶颈
    f = [[-1] * (t + 1) for _ in range(c)]
    f[0][0] = INF
    pq = [(-INF, 0, 0)]
    while pq:
        nb, u, used = heapq.heappop(pq)
        bneck = -nb
        if bneck < f[u][used]:
            continue
        for v, w in graph[u]:
            # 不升级这条边
            nxt0 = w if bneck == INF else min(bneck, w)
            if nxt0 > f[v][used]:
                f[v][used] = nxt0
                heapq.heappush(pq, (-nxt0, v, used))
            # 升级这条边，带宽变为 2w
            if used < t:
                ww = 2 * w
                nxt1 = ww if bneck == INF else min(bneck, ww)
                if nxt1 > f[v][used + 1]:
                    f[v][used + 1] = nxt1
                    heapq.heappush(pq, (-nxt1, v, used + 1))
    ans = f[c - 1][0]
    if t > 0:
        ans = max(ans, f[c - 1][t])
    if ans < 0:
        return -1
    return ans


def main():
    c, d, t = map(int, input().split())
    edges = []
    for _ in range(d):
        x, y, b = map(int, input().split())
        edges.append((x, y, b))
    print(max_bottleneck(c, t, edges))


if __name__ == "__main__":
    main()
