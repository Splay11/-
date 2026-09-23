# 区间匹配的霍尔条件：预留窗 t 当且仅当它落在某个“装满”的闭区间里


def solve(k, segs):
  # 共有 k+1 个窗。f(L,R) = 完全落在 [L,R] 内的人数
  # 若某段 f > 长度，整体无解；若 f == 长度，这段里每个窗都不能留空
  m = k + 1
  by_r = [[] for _ in range(m + 2)]
  for p, q in segs:
    by_r[q].append(p)

  # 线段树维护 h(L) = L - (左端点 < L 且右端点已加入的人数)
  size = 1
  while size < m + 2:
    size *= 2
  mx = [0] * (2 * size)
  mn = [0] * (2 * size)
  lz = [0] * (2 * size)
  for i in range(1, m + 2):
    mx[size + i] = i
    mn[size + i] = i
  for i in range(size - 1, 0, -1):
    mx[i] = mx[2 * i] if mx[2 * i] > mx[2 * i + 1] else mx[2 * i + 1]
    mn[i] = mn[2 * i] if mn[2 * i] < mn[2 * i + 1] else mn[2 * i + 1]

  def app(i, v):
    # 整段加上延迟标记
    mx[i] += v
    mn[i] += v
    lz[i] += v

  def push(i):
    if lz[i] != 0:
      app(2 * i, lz[i])
      app(2 * i + 1, lz[i])
      lz[i] = 0

  def pull(i):
    mx[i] = mx[2 * i] if mx[2 * i] > mx[2 * i + 1] else mx[2 * i + 1]
    mn[i] = mn[2 * i] if mn[2 * i] < mn[2 * i + 1] else mn[2 * i + 1]

  def add(l, r, v, i=1, L=0, R=None):
    # 区间 [l,r] 上的 h 全部加 v
    if R is None:
      R = size - 1
    if r < L or R < l:
      return
    if l <= L and R <= r:
      app(i, v)
      return
    push(i)
    mid = (L + R) // 2
    add(l, r, v, 2 * i, L, mid)
    add(l, r, v, 2 * i + 1, mid + 1, R)
    pull(i)

  def qmax(l, r, i=1, L=0, R=None):
    if R is None:
      R = size - 1
    if r < L or R < l:
      return -10 ** 18
    if l <= L and R <= r:
      return mx[i]
    push(i)
    mid = (L + R) // 2
    a = qmax(l, r, 2 * i, L, mid)
    b = qmax(l, r, 2 * i + 1, mid + 1, R)
    return a if a > b else b

  def left_eq(l, r, val, i=1, L=0, R=None):
    # [l,r] 里最左的、h 恰好等于 val 的位置
    if R is None:
      R = size - 1
    if r < L or R < l or mx[i] < val or mn[i] > val:
      return None
    if L == R:
      return L if mx[i] == val else None
    push(i)
    mid = (L + R) // 2
    a = left_eq(l, r, val, 2 * i, L, mid)
    if a is not None:
      return a
    return left_eq(l, r, val, 2 * i + 1, mid + 1, R)

  total = 0
  overflow = False
  diff = [0] * (m + 3)
  for R in range(1, m + 1):
    # 右端点等于 R 的人加入；相同左端点合并成一次区间加
    if by_r[R]:
      cnt = {}
      for p in by_r[R]:
        cnt[p] = cnt.get(p, 0) + 1
      for p, c in cnt.items():
        total += c
        if p + 1 <= m:
          add(p + 1, m, -c)
    elif overflow:
      continue
    else:
      continue
    if overflow:
      continue
    # g(L) = f(L,R) + L - (R+1) = h(L) + total - (R+1)
    gmx = qmax(1, R) + total - (R + 1)
    if gmx > 0:
      # 某段人比窗多，无论留哪个空窗都失败
      overflow = True
    elif gmx == 0:
      # 存在装满段 [L,R]，这段里的窗都不能留空
      target = (R + 1) - total
      L = left_eq(1, R, target)
      if L is not None:
        diff[L] += 1
        diff[R + 1] -= 1

  if overflow:
    return "0" * m
  ans = []
  s = 0
  for t in range(1, m + 1):
    s += diff[t]
    # 差分数 > 0 说明落在某个装满段里
    ans.append("0" if s > 0 else "1")
  return "".join(ans)


if __name__ == "__main__":
  k = int(input())
  segs = []
  for _ in range(k):
    p, q = map(int, input().split())
    segs.append((p, q))
  print(solve(k, segs))
