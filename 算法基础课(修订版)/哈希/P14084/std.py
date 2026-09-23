# 输入处理
n = int(input())  # 数组长度
a = list(map(int, input().split()))  # 数组元素

# 初始化一个字典，记录数字出现的次数
counts = {i: 0 for i in range(1, n + 1)}

# 遍历数组，计算每个数字在前缀中的出现次数
for i in range(n):
    num = a[i]
    counts[num] += 1  # 更新数字 num 的出现次数
    # 输出数字 i+1 在前缀 [a1, a2, ..., ai] 中的出现次数
    if i > 0:
        print(' ', end='')
    print(counts[i + 1], end='')
    
print()  # 输出换行
