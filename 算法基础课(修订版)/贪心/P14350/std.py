def min_groups(n, k, a):
    # 初始化分组数和当前组的最大最小值
    group_count = 1
    min_val = a[0]
    max_val = a[0]

    # 从第二个物品开始遍历
    for i in range(1, n):
        # 如果当前物品加入组后，最大值和最小值之差超过k，则需要分新的一组
        if a[i] - min_val > k or max_val - a[i] > k:
            group_count += 1
            min_val = a[i]  # 新组的最小值
            max_val = a[i]  # 新组的最大值
        else:
            # 更新当前组的最大值和最小值
            min_val = min(min_val, a[i])
            max_val = max(max_val, a[i])

    return group_count

# 输入处理
n, k = map(int, input().split())
a = list(map(int, input().split()))

# 输出结果
print(min_groups(n, k, a))
