MOD = 10**9 + 7

# 输入
n = int(input())

# 创建一个 (n+1) x (n+1) 的 dp 表
dp = [[0] * (n + 1) for _ in range(n + 1)]

# 初始化 dp[0][0] = 1
dp[0][0] = 1

# 动态规划求解
for i in range(1, n + 1):
    for j in range(0, n + 1):
        dp[i][j] = dp[i - 1][j]  # 不使用当前数 i
        if j >= i:
            dp[i][j] = (dp[i][j] + dp[i][j - i]) % MOD  # 使用当前数 i

# 输出结果
print(dp[n][n])
