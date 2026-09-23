def maxProfit(prices):
    # 初始化最大利润为 0
    max_profit = 0

    # 遍历价格数组，从第二天开始与前一天进行比较
    for i in range(1, len(prices)):
        # 如果今天的价格比昨天高，则可以获得利润
        if prices[i] > prices[i - 1]:
            # 累加利润
            max_profit += prices[i] - prices[i - 1]

    return max_profit

# 输入部分
n = int(input())  # 获取数组长度
prices = list(map(int, input().split()))  # 获取价格数组

# 输出最大利润
print(maxProfit(prices))
