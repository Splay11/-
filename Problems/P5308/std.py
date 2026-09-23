def solve(r, c, d):
  # dp[i][j]：走到 (i, j) 的最小调节能耗
  dp = [[0] * c for _ in range(r)]
  # 先填第一行：只能一路向右
  for j in range(1, c):
    dp[0][j] = dp[0][j - 1] + abs(d[0][j] - d[0][j - 1])
  # 再填第一列：只能一路向下
  for i in range(1, r):
    dp[i][0] = dp[i - 1][0] + abs(d[i][0] - d[i - 1][0])
  # 其余格子取「从上走来」和「从左走来」的较小值
  for i in range(1, r):
    for j in range(1, c):
      up = dp[i - 1][j] + abs(d[i][j] - d[i - 1][j])
      left = dp[i][j - 1] + abs(d[i][j] - d[i][j - 1])
      dp[i][j] = min(up, left)
  return dp[r - 1][c - 1]


r, c = map(int, input().split())
d = []
for _ in range(r):
  d.append(list(map(int, input().split())))
print(solve(r, c, d))
