# 从入口、出口各跑一次 Dijkstra，再枚举哪条通道免费
import heapq

INF = 10 ** 18


def dijkstra(n, src, adj):
    dist = [INF] * (n + 1)
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def min_with_one_free(n, s, t, edges, adj):
    # 入口即出口，不必移动
    if s == t:
        return 0
    ds = dijkstra(n, s, adj)
    dt = dijkstra(n, t, adj)
    # 不用协议，整段都按原长度走
    ans = ds[t]
    for u, v, w in edges:
        # 免费走 u -> v：s 到 u 的最短，加上 v 到 t 的最短
        if ds[u] < INF and dt[v] < INF:
            nd = ds[u] + dt[v]
            if nd < ans:
                ans = nd
        # 通道是双向的，另一方向同样可以免费
        if ds[v] < INF and dt[u] < INF:
            nd = ds[v] + dt[u]
            if nd < ans:
                ans = nd
    return -1 if ans >= INF else ans


def main():
    n, m, s, t = map(int, input().split())
    edges = []
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))
        adj[u].append((v, w))
        adj[v].append((u, w))
    print(min_with_one_free(n, s, t, edges, adj))


if __name__ == "__main__":
    main()
