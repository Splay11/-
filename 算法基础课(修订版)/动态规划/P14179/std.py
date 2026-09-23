import sys
s = sys.stdin.readline().strip()
n = len(s)
# dp[i][j] 代表前i+1个字符中以j为结尾的相邻两两不同的子序列个数
dp = [[0] * 10 for _ in range(n)] 
# 初始化
mod = 10 ** 9 + 7
dp[0][int(s[0])] = 1
for i in range(1, n):
    tot = 0 # 总数
    now = int(s[i])
    # 遍历前一个位置的所有字符
    for j in range(10):
        # 如果不是当前字符 . 直接等于上一个字符的个数
        if j != now:
            dp[i][j] = dp[i - 1][j]
        
        tot = (tot + dp[i - 1][j]) % mod
    # 对于当前字符，我们需要重新计算
    # 等于 总数 - 之前的字符的个数 + 1
    # 1是因为当前字符自己也是一个子序列
    dp[i][now] = (tot - dp[i - 1][now] + 1 + mod) % mod
print(sum(dp[n - 1]) % mod)
