# 读取天平物品数量
n, m = map(int, input().split())

# 读取左边天平的物品重量
left_weights = list(map(int, input().split()))

# 读取右边天平的物品重量
right_weights = list(map(int, input().split()))

# 计算左边天平的总重量
left_total = sum(left_weights)

# 计算右边天平的总重量
right_total = sum(right_weights)

# 比较两个天平的总重量并输出结果
if left_total == right_total:
    print("Equal")
else:
    print("Not Equal")
