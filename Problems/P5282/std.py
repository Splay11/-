def max_sum_len_ge(a, L):
  """一维数组中长度至少为 L 的连续段最大和"""
  n = len(a)
  if n < L:
    return None
  P = [0] * (n + 1)
  for i in range(n):
    P[i + 1] = P[i] + a[i]
  best = P[L] - P[0]
  mn = P[0]
  for r in range(L, n + 1):
    s = P[r] - mn
    if s > best:
      best = s
    nxt = r - L + 1
    if nxt <= n and P[nxt] < mn:
      mn = P[nxt]
  return best


def solve(n, m, grid):
  ans = -10**18
  # 枚举上下界，此时行数 h 固定；要求列宽 w>=h，则 k=h
  for top in range(n):
    col = [0] * m
    for bottom in range(top, n):
      h = bottom - top + 1
      for j in range(m):
        col[j] += grid[bottom][j]
      s = max_sum_len_ge(col, h)
      if s is not None:
        v = h * s
        if v > ans:
          ans = v
  # 枚举左右界，此时列数 w 固定；要求行高 h>=w，则 k=w
  for left in range(m):
    row = [0] * n
    for right in range(left, m):
      w = right - left + 1
      for i in range(n):
        row[i] += grid[i][right]
      s = max_sum_len_ge(row, w)
      if s is not None:
        v = w * s
        if v > ans:
          ans = v
  return ans


if __name__ == "__main__":
  n, m = map(int, input().split())
  grid = [list(map(int, input().split())) for _ in range(n)]
  print(solve(n, m, grid))
