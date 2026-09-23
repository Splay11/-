def fractional_knapsack(n, C, items):
    # 计算每个商品的单位重量价值
    items_with_ratio = []
    for weight, value in items:
        ratio = value / weight  # 计算单位重量的价值
        items_with_ratio.append((weight, value, ratio))
    
    # 按照单位重量价值从大到小排序
    items_with_ratio.sort(key=lambda x: x[2], reverse=True)
    
    total_value = 0.0  # 总价值初始化为0
    remaining_capacity = C  # 剩余背包容量
    
    for weight, value, ratio in items_with_ratio:
        if remaining_capacity == 0:  # 背包已满
            break
        if weight <= remaining_capacity:  # 商品能完全放入背包
            total_value += value
            remaining_capacity -= weight
        else:  # 只能放入部分商品
            total_value += value * (remaining_capacity / weight)
            remaining_capacity = 0  # 背包满了
    
    # 输出最终的总价值，保留两位小数
    return round(total_value, 2)

# 输入部分
n, C = map(int, input().split())  # 读取商品数量n和背包最大承重C
items = []

for _ in range(n):
    w, v = map(int, input().split())  # 读取每个商品的重量w和价值v
    items.append((w, v))

# 计算并输出结果
result = fractional_knapsack(n, C, items)
print(f"{result:.2f}")
