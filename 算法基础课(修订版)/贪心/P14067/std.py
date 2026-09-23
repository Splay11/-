def max_activities(n, activities):
    # 1. 按照活动的结束时间排序
    activities.sort(key=lambda x: x[1])
    
    # 2. 初始化选中的活动数量和上一个活动的结束时间
    count = 0
    last_end_time = -1
    
    # 3. 遍历所有活动，选择不与前一个活动重叠的活动
    for start, end in activities:
        # 如果当前活动的开始时间大于上一个活动的结束时间
        if start > last_end_time:
            count += 1  # 选择该活动
            last_end_time = end  # 更新上一个活动的结束时间为当前活动的结束时间
    
    return count

# 输入处理部分
n = int(input())  # 活动数量
activities = []
for _ in range(n):
    start, end = map(int, input().split())  # 每个活动的开始时间和结束时间
    activities.append((start, end))

# 输出最多可以选择的活动数
print(max_activities(n, activities))
