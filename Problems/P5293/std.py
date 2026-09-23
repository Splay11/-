import heapq


def solve(n, F, p, edges):
  # 建无向图：边权为 (耗能, 耗时)
  g = [[] for _ in range(n + 1)]
  for u, v, c, t in edges:
    g[u].append((v, c, t))
    g[v].append((u, c, t))
  # dist[u][f]：到达城市 u 且剩余油量为 f 的最短时间
  INF = 10 ** 18
  dist = [[INF] * (F + 1) for _ in range(n + 1)]
  # 出发时油箱是满的，不花时间
  dist[1][F] = 0
  pq = [(0, 1, F)]
  while pq:
    d, u, f = heapq.heappop(pq)
    if d != dist[u][f]:
      continue
    # Dijkstra 第一次弹出终点即为最短
    if u == n:
      return d
    # 在当前城市加 1 单位油，油量不能超过容量 F
    if f < F:
      nd = d + p[u]
      if nd < dist[u][f + 1]:
        dist[u][f + 1] = nd
        heapq.heappush(pq, (nd, u, f + 1))
    # 剩余油够就走邻接边
    for v, c, t in g[u]:
      if f >= c:
        nd = d + t
        nf = f - c
        if nd < dist[v][nf]:
          dist[v][nf] = nd
          heapq.heappush(pq, (nd, v, nf))
  return -1


if __name__ == "__main__":
  # 第一行点数、边数、油箱容量；第二行各城加油耗时；随后 m 条双向边
  n, m, F = map(int, input().split())
  p = [0] + list(map(int, input().split()))
  edges = []
  for _ in range(m):
    u, v, c, t = map(int, input().split())
    edges.append((u, v, c, t))
  print(solve(n, F, p, edges))
