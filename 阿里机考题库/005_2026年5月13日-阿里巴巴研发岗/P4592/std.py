# -*- coding: utf-8 -*-
"""特权节点路径 — 到达特权节点后所有边免费
算法：
1. Dijkstra 从起点(0)求最短代价（边权 = 安全等级 w）
2. 反向 BFS 从终点(n-1)标记能到达终点的节点
3. 枚举特权节点：若可到终点，取最小 dist[p]

复杂度：O((n+m) log n)
"""
import sys
import heapq
from collections import deque

INF = 10 ** 18


def main() -> None:
    # 快速读入所有数据
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))  # 节点数
    m = int(next(it))  # 边数
    k = int(next(it))  # 特权节点数

    # 读入特权节点
    lucky = [False] * n
    lucky_nodes = []
    for _ in range(k):
        r = int(next(it)) - 1  # 转为 0-based
        lucky[r] = True
        lucky_nodes.append(r)

    # 建图：正向图 + 反向图（反向图仅判断连通性，不带权）
    g = [[] for _ in range(n)]   # 正向邻接表: (v, w)
    rg = [[] for _ in range(n)]  # 反向邻接表: 仅存节点编号

    for _ in range(m):
        u = int(next(it)) - 1  # 起点（0-based）
        v = int(next(it)) - 1  # 终点（0-based）
        w = int(next(it))      # 安全等级（直接用 1-based 值）
        g[u].append((v, w))
        rg[v].append(u)        # 反向边

    # ---- 第一步：Dijkstra 求起点到各点的最小开销 ----
    dist = [INF] * n
    dist[0] = 0  # 起点为节点 1（即下标 0）
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue  # 过期状态，跳过
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    # ---- 第二步：反向 BFS 标记能到达终点的节点 ----
    can_reach = [False] * n
    can_reach[n - 1] = True  # 终点自身可达
    q = deque([n - 1])
    while q:
        u = q.popleft()
        for v in rg[u]:       # 沿反向边走
            if not can_reach[v]:
                can_reach[v] = True
                q.append(v)

    # ---- 第三步：枚举特权节点取最小值 ----
    ans = INF
    for p in lucky_nodes:
        if can_reach[p] and dist[p] < ans:
            ans = dist[p]

    print(-1 if ans >= INF else ans)


if __name__ == "__main__":
    main()
