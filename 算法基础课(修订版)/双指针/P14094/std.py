def find_two_sum(nums, target):
    left = 0
    right = len(nums) - 1
    
    while left < right:
        # 计算当前左指针和右指针所指元素的和
        sum_val = nums[left] + nums[right]
        
        if sum_val == target:
            # 找到符合条件的下标，注意转换为从1开始的下标
            return left + 1, right + 1  # 返回1-based索引
        elif sum_val < target:
            # 当前和小于目标值，左指针右移
            left += 1
        else:
            # 当前和大于目标值，右指针左移
            right -= 1
    
    # 如果没有找到符合条件的两个数
    return -1

# 读取输入
n = int(input())  # 数组的长度
nums = list(map(int, input().split()))  # 排序数组
target = int(input())  # 目标值

# 调用函数
result = find_two_sum(nums, target)

# 输出结果
if result == -1:
    print(-1)
else:
    print(result[0], result[1])
