def max_aesthetic_value(n, m, a, b, c):
    # 创建一个大小为 m+1 的列表，用于存储每个标签对应的物品索引
    idx = [[] for _ in range(m + 1)]
    
    # 将每个物品根据它适合的标签分类存储
    for i in range(n):
        idx[a[i]].append(i)
    
    total_value = 0  # 初始化总美观值为0
    
    # 对每个标签所对应的物品进行处理
    for lst in idx:
        if not lst:
            continue  # 如果某个标签没有对应物品，跳过
        
        # 对标签对应的物品按 b[i] - c[i] 降序排序
        lst.sort(key=lambda x: c[x] - b[x])  # 先贴标签的美观值优先
        
        # 给第一个物品贴标签，选择 b[i] 或 c[i] 中更大的值
        total_value += max(b[lst[0]], c[lst[0]])  # 优先选择贴标签
        
        # 处理剩下的物品，全部选择不贴标签的美观值
        for i in lst[1:]:
            total_value += c[i]  # 剩下的物品选择不贴标签
    
    return total_value  # 返回总美观值

# 输入部分
n, m = map(int, input().split())  # 物品数量 n，标签种类 m
a = list(map(int, input().split()))  # 每个物品适合的标签
b = list(map(int, input().split()))  # 每个物品贴上适合标签后的美观值
c = list(map(int, input().split()))  # 每个物品不贴上适合标签时的美观值

# 计算最大美观值
result = max_aesthetic_value(n, m, a, b, c)

# 输出结果
print(result)
