import sys
import json

# 读取整行输入，形如：[..warehouses..][[..queries..]]N
line = sys.stdin.read().strip()


def match_bracket(s, start):
    """返回从 start 处的 '[' 匹配的 ']' 的下标。"""
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '[':
            depth += 1
        elif s[i] == ']':
            depth -= 1
            if depth == 0:
                return i
    return -1


# 解析 warehouses（第一个 [...] 一维数组）
p1 = line.index('[')
e1 = match_bracket(line, p1)
warehouses = json.loads(line[p1:e1 + 1])

# 解析 queries（第二个 [[...]] 二维数组）
p2 = line.index('[', e1 + 1)
e2 = match_bracket(line, p2)
queries = json.loads(line[p2:e2 + 1])

# 解析末尾整数 numOfWarehouse
numOfWarehouse = int(line[e2 + 1:].strip())

res = Solution().getWarehouseReport(warehouses, queries, numOfWarehouse)

# 按题目样例格式紧凑输出，如 [[16,1,0]]
print('[' + ','.join('[' + ','.join(str(x) for x in row) + ']' for row in res) + ']')
