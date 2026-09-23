def solve(k, t, s):
  # 在硐口 i 接通后，矿石再走 s[i]，值班员走 t
  # 等待就是多出来的时间，不能为负
  ans = []
  for i in range(k):
    wait = s[i] - t
    if wait < 0:
      wait = 0
    ans.append(wait)
  return ans


# 第一行硐口数和步行时间，第二行各硐口到卸矿平台的路程
k, t = map(int, input().split())
s = list(map(int, input().split()))
ans = solve(k, t, s)
print(" ".join(str(x) for x in ans))
