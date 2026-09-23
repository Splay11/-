import sys
from collections import deque

def solve_one(cnt, seed, mod_set):
  mn = min(mod_set)
  max_mod = max(mod_set)

  # 种子已小于最小模数，后续折减均不改变当前值
  if seed < mn:
    return seed

  mods = list(set(mod_set))
  vis = [False] * (max_mod + 1)
  q = deque()

  # 第一次有效折减：seed mod order_i
  for a in mods:
    if a <= seed:
      r = seed % a
      if not vis[r]:
        vis[r] = True
        q.append(r)

  # BFS 枚举所有可达的 cur
  while q:
    cur = q.popleft()
    for a in mods:
      if a <= cur:
        nxt = cur % a
        if not vis[nxt]:
          vis[nxt] = True
          q.append(nxt)

  # 最终余值必须严格小于 mn
  ans = 0
  for i in range(mn):
    if vis[i]:
      ans = i
  return ans

data = list(map(int, sys.stdin.buffer.read().split()))
idx = 0
T = data[idx]
idx += 1
res = []

for _ in range(T):
  cnt = data[idx]
  seed = data[idx + 1]
  idx += 2
  mod_set = data[idx:idx + cnt]
  idx += cnt
  res.append(str(solve_one(cnt, seed, mod_set)))

print("\n".join(res))
