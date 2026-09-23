import heapq

INF = 10**30


def min_time(n, roads, portals, cap, src, dst):
    # 起点等于终点：不必移动
    if src == dst:
        return 0
    # 普通巷道邻接表
    g = [[] for _ in range(n)]
    for u, v, d in roads:
        g[u].append((v, d))
        g[v].append((u, d))
    # 罐笼邻接表（耗时 0）
    pg = [[] for _ in range(n)]
    for u, v in portals:
        pg[u].append(v)
        pg[v].append(u)
    # dist[工位][已用罐笼次数][上一步是否罐笼]
    dist = [[[INF, INF] for _ in range(cap + 1)] for _ in range(n)]
    dist[src][0][0] = 0
    pq = [(0, src, 0, 0)]
    while pq:
        cur, u, used, last = heapq.heappop(pq)
        if cur != dist[u][used][last]:
            continue
        if u == dst:
            return cur
        # 走普通巷道：结束后“上一步不是罐笼”，次数不变
        for v, d in g[u]:
            nd = cur + d
            if nd < dist[v][used][0]:
                dist[v][used][0] = nd
                heapq.heappush(pq, (nd, v, used, 0))
        # 坐罐笼：不能连坐，且次数还没用完；出发时 last=0 所以可以直接坐
        if last == 0 and used < cap:
            for v in pg[u]:
                if cur < dist[v][used + 1][1]:
                    dist[v][used + 1][1] = cur
                    heapq.heappush(pq, (cur, v, used + 1, 1))
    return -1


def main():
    n, m = map(int, input().split())
    roads = []
    for _ in range(m):
        u, v, d = map(int, input().split())
        roads.append((u, v, d))
    p = int(input())
    portals = []
    for _ in range(p):
        u, v = map(int, input().split())
        portals.append((u, v))
    cap, src, dst = map(int, input().split())
    print(min_time(n, roads, portals, cap, src, dst))


if __name__ == "__main__":
    main()
