import sys

# 读取整行输入，格式：N,K,M,[a1,a2,...,aN]
line = sys.stdin.read().strip()

# 找到第一个逗号，解析 N
pos1 = line.find(',')
N = int(line[:pos1])

# 找到第二个逗号，解析 K
pos2 = line.find(',', pos1 + 1)
K = int(line[pos1 + 1:pos2])

# 找到第三个逗号，解析 M
pos3 = line.find(',', pos2 + 1)
M = int(line[pos2 + 1:pos3])

# 解析数组部分
arr_str = line[pos3 + 1:].strip()
# 去除方括号
if arr_str.startswith('['):
    arr_str = arr_str[1:]
if arr_str.endswith(']'):
    arr_str = arr_str[:-1]

if arr_str:
    A = [int(x.strip()) for x in arr_str.split(',')]
else:
    A = []

# 调用用户代码
print(Solution().maxSpiritPower(N, K, M, A))
