n = int(input())  # 读取输入的整数n，表示数组的长度
a = list(map(int, input().split()))  # 读取n个整数，存储在列表a中

dp = [0] * (n + 1)  # 初始化前缀和数组dp，长度为n+1，dp[0]设为0

# 计算前缀和
for i in range(1, n + 1):
    dp[i] = dp[i - 1] + a[i - 1]  # 当前前缀和等于前一个前缀和加上当前元素
    print(dp[i])  # 输出当前的前缀和
