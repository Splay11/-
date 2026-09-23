# 读取输入
n = int(input())  # 输入一个整数 n，表示硬币的种类数
coins = list(map(int, input().split()))  # 输入 n 个整数，表示每种硬币的面值
amount = int(input())  # 输入一个整数 amount，表示目标金额

# 初始化动态规划数组
# dp[i] 表示组成金额 i 所需的最少硬币个数
# 初始时，除了 dp[0] = 0，其余都设置为一个较大的数，表示尚未达到
dp = [float('inf')] * (amount + 1)
dp[0] = 0  # 金额为 0 时，不需要任何硬币

# 遍历每一个硬币
for coin in coins:
    # 从当前硬币面值到目标金额进行遍历
    for x in range(coin, amount + 1):
        if dp[x - coin] + 1 < dp[x]:
            dp[x] = dp[x - coin] + 1
            # 解释：
            # 如果使用当前硬币 coin 后，组成金额 x 所需的硬币数比之前记录的 dp[x] 更少，
            # 则更新 dp[x] 为 dp[x - coin] + 1

# 判断并输出结果
if dp[amount] == float('inf'):
    print(-1)  # 如果 dp[amount] 仍为无穷大，表示无法组成该金额
else:
    print(dp[amount])  # 输出组成金额 amount 所需的最少硬币个数
