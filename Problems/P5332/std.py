import numpy as np

INF = 10 ** 18


def solve(k, q, w, v):
  # 每个小时只需要上调 0..q-1。相邻复盘窗口相差一小时，上调量沿步长 w 的链被模关系钉死
  # 第一段 w 个起点的上调量在模 q 下求和要凑满第一个窗口，用最小费用和卷积求出
  if w == 1:
    # 每个单格自己就要被 q 整除
    return int(sum((-x) % q for x in v))
  pref = [0] * (k + 1)
  for i in range(k):
    pref[i + 1] = pref[i] + v[i]
  nwin = k - w + 1
  s = [(pref[p + w] - pref[p]) % q for p in range(nwin)]
  need = (-s[0]) % q
  if w == k:
    # 只有一个窗，把差额补到任意一格即可
    return need

  chain = np.zeros((w, q), dtype=np.int64)
  for r in range(w):
    # 第 r 条链：起点补 x 时，后面每一格都是 (x + 固定偏移) mod q
    offs = [0]
    off = 0
    p = r
    while p + w < k:
      off = (off + s[p] - s[p + 1]) % q
      offs.append(off)
      p += w
    c = len(offs)
    sm = sum(offs)
    cnt = [0] * q
    for o in offs:
      if o:
        # x >= q-o 时这一格会再减一个 q
        cnt[q - o] += 1
    acc = 0
    wrap = [0] * q
    for x in range(q):
      acc += cnt[x]
      wrap[x] = acc
    for x in range(q):
      chain[r, x] = c * x + sm - q * wrap[x]

  dp = np.full(q, INF, dtype=np.int64)
  dp[0] = 0
  for r in range(w):
    # ndp[(md+x) mod q] = min(dp[md] + 第 r 条链选 x 的费用)
    ndp = np.full(q, INF, dtype=np.int64)
    c = chain[r]
    for x in range(q):
      cx = int(c[x])
      if x == 0:
        ndp = np.minimum(ndp, dp + cx)
      else:
        ndp[x:] = np.minimum(ndp[x:], dp[: q - x] + cx)
        ndp[:x] = np.minimum(ndp[:x], dp[q - x:] + cx)
    dp = ndp
  return int(dp[need])


if __name__ == "__main__":
  k, q, w = map(int, input().split())
  v = list(map(int, input().split()))
  print(solve(k, q, w, v))
