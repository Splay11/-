def solve(k, u, v, g, h):
  # 渗水量从大到小排：封堵令给最大的，引流令给接下来的
  h = sorted(h, reverse=True)
  ans = 0
  for i in range(k):
    if i < u:
      # 封堵，该点残留为 0
      continue
    if i < u + v:
      # 引流，减去固定幅度 g，不能减成负数
      val = h[i] - g
      if val < 0:
        val = 0
      ans += val
    else:
      # 暂缓，残留就是原渗水量
      ans += h[i]
  return ans


# 第一行四个整数，第二行 k 个渗水量
k, u, v, g = map(int, input().split())
h = list(map(int, input().split()))
print(solve(k, u, v, g, h))
