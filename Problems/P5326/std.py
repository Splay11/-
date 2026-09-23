def solve(w):
  # 对每个色号，先丢掉比它大的格子，再数它自己的连续段
  # 更大色号后喷，不会隔开当前这一次喷涂
  ans = 0
  for c in range(26):
    ch = chr(ord("a") + c)
    in_run = False
    for x in w:
      if x > ch:
        continue
      if x == ch:
        if not in_run:
          ans += 1
          in_run = True
      else:
        # 碰到更小色号，当前段被已经喷好的格子隔开
        in_run = False
  return ans


w = input().strip()
print(solve(w))
