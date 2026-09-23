def solve(w):
  # 扫一遍，相邻同色就断开，统计当前段长度
  best = 1
  cur = 1
  for i in range(1, len(w)):
    if w[i] != w[i - 1]:
      cur += 1
      if cur > best:
        best = cur
    else:
      cur = 1
  return best


w = input().strip()
print(solve(w))
