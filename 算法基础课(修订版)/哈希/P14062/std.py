def count_pairs(n, p):
    # 创建一个哈希表，用于记录 p_i - i 出现的次数
    diff_count = {}
    # 结果变量，记录符合条件的(i, j)对数
    result = 0
    
    for j in range(n):
        # 计算 j - p_j
        diff = (j + 1) - p[j]
        # 如果 -diff 已经出现过，那么就说明存在符合条件的 i
        if -diff in diff_count:
            result += diff_count[-diff]
        
        # 更新 diff_count
        if diff in diff_count:
            diff_count[diff] += 1
        else:
            diff_count[diff] = 1
    
    return result

# 输入读取
n = int(input())
p = list(map(int, input().split()))

# 调用函数并输出结果
print(count_pairs(n, p))
