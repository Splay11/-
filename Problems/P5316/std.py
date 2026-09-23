import heapq
from collections import defaultdict


class LazyHeap:
  def __init__(self, want_max):
    self.h = []
    self.cnt = defaultdict(int)
    self.want_max = want_max

  def add(self, x):
    # 大根堆用取负来模拟
    if self.want_max:
      x = -x
    heapq.heappush(self.h, x)
    self.cnt[x] += 1

  def remove(self, x):
    # 懒删除：只改计数，真正弹出放到取堆顶时
    if self.want_max:
      x = -x
    self.cnt[x] -= 1

  def top(self):
    while self.h and self.cnt[self.h[0]] == 0:
      heapq.heappop(self.h)
    if not self.h:
      return None
    x = self.h[0]
    if self.want_max:
      return -x
    return x


def solve(w, v, caps, floors):
  # 稀释闸 [L,R] 上界 c：L 加入，R+1 删除
  add_c = [[] for _ in range(w + 2)]
  del_c = [[] for _ in range(w + 2)]
  for L, R, c in caps:
    add_c[L].append(c)
    del_c[R + 1].append(c)
  # 回灌泵 [L,R] 下界 d：同样拆成端点事件
  add_d = [[] for _ in range(w + 2)]
  del_d = [[] for _ in range(w + 2)]
  for L, R, d in floors:
    add_d[L].append(d)
    del_d[R + 1].append(d)
  # 稀释取最小上界，回灌取最大下界
  hc = LazyHeap(False)
  hd = LazyHeap(True)
  inf = 10 ** 18
  e = [0] * w
  for i in range(1, w + 1):
    for x in del_c[i]:
      hc.remove(x)
    for x in add_c[i]:
      hc.add(x)
    for x in del_d[i]:
      hd.remove(x)
    for x in add_d[i]:
      hd.add(x)
    hi = hc.top()
    if hi is None:
      hi = inf
    lo = hd.top()
    if lo is None:
      lo = 0
    val = v[i - 1]
    if val < lo:
      val = lo
    if val > hi:
      val = hi
    e[i - 1] = val
  return e


w, x, y = map(int, input().split())
v = list(map(int, input().split()))
caps = []
for _ in range(x):
  L, R, c = map(int, input().split())
  caps.append((L, R, c))
floors = []
for _ in range(y):
  L, R, d = map(int, input().split())
  floors.append((L, R, d))
e = solve(w, v, caps, floors)
print(" ".join(str(z) for z in e))
