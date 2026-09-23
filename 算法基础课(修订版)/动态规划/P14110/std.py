# 读取数组的长度
n = int(input())  # 输入一个整数 n，表示数组的长度

# 读取数组元素并转换为整数列表
a = list(map(int, input().split()))  # 输入 n 个整数并存储在列表 a 中

# 初始化动态规划数组 dp，长度为 n+1，所有值初始为 1
dp = [1] * (n + 1)  # dp[i] 表示以第 i 个元素结尾的最长递增子序列的长度

# 遍历每个元素，计算最长递增子序列
for i in range(n):
    # 遍历当前元素之前的所有元素
    for j in range(i):
        # 如果当前元素 a[i] 大于之前的元素 a[j]
        if a[i] > a[j]:
            # 更新 dp[i] 为 dp[j] + 1 或当前 dp[i] 的最大值
            dp[i] = max(dp[i], dp[j] + 1)

# 输出 dp 数组中的最大值，即最长递增子序列的长度
print(max(dp))  # 输出结果
