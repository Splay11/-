import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 找到顶层逗号：追踪括号深度，找第一个深度 0 处的逗号
depth = 0
comma_pos = -1
for i, ch in enumerate(line):
    if ch == '[':
        depth += 1
    elif ch == ']':
        depth -= 1
    elif ch == ',' and depth == 0:
        comma_pos = i
        break

data_str = line[:comma_pos]
interval = int(line[comma_pos + 1:])

data = ast.literal_eval(data_str)

# 调用用户代码
result = Solution().getMaxValues(data, interval)
print(str(result).replace(' ', ''))
