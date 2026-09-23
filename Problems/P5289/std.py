def solve(n, edges):
  # 只有一个点时无处可走
  if n == 1:
    return 0
  # 建无向树，同时累加全部边权
  g = [[] for _ in range(n + 1)]
  total = 0
  for u, v, w in edges:
    g[u].append((v, w))
    g[v].append((u, w))
    total += w
  # 从 1 号队部做一遍遍历，算出到每个哨所的距离
  dist = [-1] * (n + 1)
  dist[1] = 0
  stack = [1]
  while stack:
    u = stack.pop()
    for v, w in g[u]:
      if dist[v] < 0:
        dist[v] = dist[u] + w
        stack.append(v)
  # 除通往最远哨所的链外，每条边都要走一个来回
  farthest = 0
  for i in range(1, n + 1):
    if dist[i] > farthest:
      farthest = dist[i]
  return 2 * total - farthest


if __name__ == "__main__":
  # 第一行点数，随后 n-1 条边
  n = int(input())
  edges = []
  for _ in range(n - 1):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))
  print(solve(n, edges))
