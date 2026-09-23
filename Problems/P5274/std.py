from collections import deque


def solve(n, edges):
  # 无向无权图：邻接表存双向边
  g = [[] for _ in range(n + 1)]
  for u, v in edges:
    g[u].append(v)
    g[v].append(u)
  # dist[i] = -1 表示还没走到；门厅 1 号距离为 0
  dist = [-1] * (n + 1)
  dist[1] = 0
  q = deque([1])
  while q:
    u = q.popleft()
    for v in g[u]:
      if dist[v] < 0:
        dist[v] = dist[u] + 1
        q.append(v)
  # 只收集可达点，按（距离，编号）排序
  arr = []
  for i in range(1, n + 1):
    if dist[i] >= 0:
      arr.append((dist[i], i))
  arr.sort()
  return arr


if __name__ == "__main__":
  n, m = map(int, input().split())
  edges = []
  for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))
  ans = solve(n, edges)
  for d, i in ans:
    print(i, d)
