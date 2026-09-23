def minCoins(coins, amount):
    # 将硬币按面额从大到小排序
    coins.sort(reverse=True)
    
    # 初始化硬币数目
    coin_count = 0
    
    # 遍历硬币，尝试从大到小使用硬币
    for coin in coins:
        if amount == 0:
            break
        # 使用尽可能多的当前硬币
        coin_count += amount // coin
        amount %= coin  # 更新剩余金额
    
    # 如果amount变为0，说明找到了最小硬币数
    if amount == 0:
        return coin_count
    else:
        return -1  # 如果无法组合成目标金额，返回-1

# 输入处理部分
n = int(input())  # 硬币数量
coins = list(map(int, input().split()))  # 硬币面额
amount = int(input())  # 目标金额

# 输出最少硬币数
print(minCoins(coins, amount))
