def pick_median(pts):
  # 按坐标排序后，累加人数，找到加权中位数
  pts.sort(key=lambda t: t[0])
  tot = 0
  for pos, w in pts:
    tot += w
  acc = 0
  for pos, w in pts:
    acc += w
    # 前缀人数第一次达到总人数的一半，就是最优落点
    if acc * 2 >= tot:
      return pos
  return pts[-1][0]


def solve(m, a, b, w):
  xs = []
  ys = []
  for i in range(m):
    xs.append((a[i], w[i]))
    ys.append((b[i], w[i]))
  # 横、纵分别取加权中位数
  P = pick_median(xs)
  Q = pick_median(ys)
  ans = 0
  for i in range(m):
    ans += w[i] * (abs(a[i] - P) + abs(b[i] - Q))
  return ans


m = int(input())
a = []
b = []
w = []
for _ in range(m):
  ai, bi, wi = map(int, input().split())
  a.append(ai)
  b.append(bi)
  w.append(wi)
print(solve(m, a, b, w))
