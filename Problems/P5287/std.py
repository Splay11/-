import heapq

INF = 10**18


def dijkstra(n, g, src):
  dist = [INF] * (n + 1)
  dist[src] = 0
  pq = [(0, src)]
  while pq:
    d, u = heapq.heappop(pq)
    if d != dist[u]:
      continue
    for v, w in g[u]:
      nd = d + w
      if nd < dist[v]:
        dist[v] = nd
        heapq.heappush(pq, (nd, v))
  return dist


def solve(n, s, g, a, b, dests):
  nodes = [s] + dests
  uniq = []
  seen = set()
  for x in nodes:
    if x not in seen:
      seen.add(x)
      uniq.append(x)
  table = {}
  for u in uniq:
    table[u] = dijkstra(n, g, u)
  t = 0
  cur = s
  for d in dests:
    t += table[cur][d]
    if t % 2 == 1:
      t += a
    else:
      t += b
    cur = d
  t += table[cur][s]
  return t


if __name__ == "__main__":
  n, m, k, s = map(int, input().split())
  g = [[] for _ in range(n + 1)]
  for _ in range(m):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
  for _ in range(k):
    u, v, w = map(int, input().split())
    g[u].append((v, w))
    g[v].append((u, w))
  a, b, q = map(int, input().split())
  dests = list(map(int, input().split()))
  print(solve(n, s, g, a, b, dests))
