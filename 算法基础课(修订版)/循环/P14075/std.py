# 读取数组大小
n = int(input())

# 读取数组元素
arr = list(map(int, input().split()))

# 找出最大值
max_value = max(arr)

# 找出所有最大值的下标
indices = [str(index) for index, value in enumerate(arr) if value == max_value]

# 输出最大值
print(max_value)

# 输出所有最大值的下标，空格分隔
print(' '.join(indices))
