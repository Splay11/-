n = int(input())  # 输入整数 n
a = list(map(int, input().split()))  # 输入 n 个整数到列表 a 中

# 输出数组 a 的所有元素，空格分隔
print(' '.join([str(_) for _ in a]),end='')  
# 避免最后一个元素后有空格
