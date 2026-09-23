import heapq


def solve(k, q, r, edges):
  # 状态 (城市, 剩余油量)，边权是时间
  g = [[] for _ in range(k + 1)]
  for a, b, c, t in edges:
    g[a].append((b, c, t))
    g[b].append((a, c, t))
  inf = 10 ** 18
  dist = [[inf] * (q + 1) for _ in range(k + 1)]
  # 出发时油箱是满的
  dist[1][q] = 0
  h = [(0, 1, q)]
  while h:
    tm, u, f = heapq.heappop(h)
    if tm != dist[u][f]:
      continue
    # 在当前城加 1 单位油
    if f < q:
      nf = f + 1
      ntm = tm + r[u - 1]
      if ntm < dist[u][nf]:
        dist[u][nf] = ntm
        heapq.heappush(h, (ntm, u, nf))
    # 有油就走相邻路
    for v, c, t in g[u]:
      if f >= c:
        nf = f - c
        ntm = tm + t
        if ntm < dist[v][nf]:
          dist[v][nf] = ntm
          heapq.heappush(h, (ntm, v, nf))
  ans = min(dist[k])
  if ans >= inf:
    return -1
  return ans


first = list(map(int, input().split()))
k, e, q = first
r = list(map(int, input().split()))
edges = []
for _ in range(e):
  a, b, c, t = map(int, input().split())
  edges.append((a, b, c, t))
print(solve(k, q, r, edges))
