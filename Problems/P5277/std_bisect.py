# bisect 维护去重坐标，每次 O(N) 扫间隙
from bisect import bisect_left, insort

n, m = map(int, input().split())
b = list(map(int, input().split()))
cnt = {}
coords = []
for v in b:
  cnt[v] = cnt.get(v, 0) + 1
  if cnt[v] == 1:
    insort(coords, v)


def calc_w():
  ans = 0
  for i in range(len(coords) - 1):
    ans = max(ans, (coords[i + 1] - coords[i]) // 2)
  return ans


for _ in range(m):
  r, z = map(int, input().split())
  old = b[r - 1]
  if old != z:
    cnt[old] -= 1
    if cnt[old] == 0:
      del cnt[old]
      coords.pop(bisect_left(coords, old))
    b[r - 1] = z
    if z in cnt:
      cnt[z] += 1
    else:
      cnt[z] = 1
      insort(coords, z)
  print(calc_w())
