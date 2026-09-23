from collections import deque


def solve(r, c, sx, sy, a):
  # 起点是陆地，无法逃生
  if a[sx][sy] == 1:
    return None
  inf = 10 ** 9
  dist = [[inf] * c for _ in range(r)]
  rsum = [[0] * c for _ in range(r)]
  csum = [[0] * c for _ in range(r)]
  parent = [[None] * c for _ in range(r)]
  dist[sx][sy] = 0
  rsum[sx][sy] = sx
  csum[sx][sy] = sy
  q = deque()
  q.append((sx, sy))
  dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  while q:
    x, y = q.popleft()
    for dx, dy in dirs:
      nx = x + dx
      ny = y + dy
      if nx < 0 or nx >= r or ny < 0 or ny >= c:
        continue
      if a[nx][ny] != 0:
        continue
      nd = dist[x][y] + 1
      nrs = rsum[x][y] + nx
      ncs = csum[x][y] + ny
      # 更短，或者同样短但行号和/列号和更优，则更新
      if nd < dist[nx][ny]:
        dist[nx][ny] = nd
        rsum[nx][ny] = nrs
        csum[nx][ny] = ncs
        parent[nx][ny] = (x, y)
        q.append((nx, ny))
      elif nd == dist[nx][ny]:
        if (nrs, ncs) < (rsum[nx][ny], csum[nx][ny]):
          rsum[nx][ny] = nrs
          csum[nx][ny] = ncs
          parent[nx][ny] = (x, y)
  best = None
  for i in range(r):
    for j in range(c):
      if dist[i][j] >= inf:
        continue
      # 边界水域才算出岛
      if i == 0 or i == r - 1 or j == 0 or j == c - 1:
        cur = (dist[i][j], i, j)
        if best is None or cur < best:
          best = cur
  if best is None:
    return None
  d, ei, ej = best
  path = []
  cur = (ei, ej)
  while cur is not None:
    path.append(cur)
    cur = parent[cur[0]][cur[1]]
  path.reverse()
  return path


r, c = map(int, input().split())
sx, sy = map(int, input().split())
a = []
for _ in range(r):
  a.append(list(map(int, input().split())))
path = solve(r, c, sx, sy, a)
if path is None:
  print(-1)
else:
  print(len(path) - 1)
  for x, y in path:
    print(x, y)
