def solve(k, q, x, y):
  # (x+y) mod q = x+y 或 x+y-q，总残差 = sum(x)+sum(y) - q * 进位次数
  # 要最小总残差，就要让尽量多的工单对满足 x+y >= q
  xs = sorted(x)
  ys = sorted(y)
  i = k - 1
  j = 0
  wrap = 0
  # 从大到小看研发侧，配上还能进位的最小测试侧收益
  while i >= 0 and j < k:
    if xs[i] + ys[j] >= q:
      wrap += 1
      i -= 1
      j += 1
    else:
      # 这个测试侧收益连当前最大研发侧都凑不齐，后面更小的更不行
      j += 1
  return sum(xs) + sum(ys) - wrap * q


if __name__ == "__main__":
  k, q = map(int, input().split())
  x = list(map(int, input().split()))
  y = list(map(int, input().split()))
  print(solve(k, q, x, y))
