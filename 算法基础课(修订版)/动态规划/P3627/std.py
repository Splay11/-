n = int(input())
MOD = 10**9 + 7

# 初始化二维DP数组
dp = [[0] * (n + 1) for _ in range(n + 1)]
dp[0][0] = 1  # 初始条件

for i in range(1, n + 1):  # 考虑数字1到n
    for j in range(n + 1):  # 计算组成0到n的方案数
        dp[i][j] = dp[i - 1][j]  # 不选数字i的方案数
        if j >= i:
            dp[i][j] = (dp[i][j] + dp[i - 1][j - i]) % MOD  # 选数字i的方案数

print(dp[n][n])
