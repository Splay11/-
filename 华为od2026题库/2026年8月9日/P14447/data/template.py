import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 顶层逗号查找（不在括号内的逗号）
def find_top_level_comma(s):
    bracket = 0
    for i, c in enumerate(s):
        if c == '[':
            bracket += 1
        elif c == ']':
            bracket -= 1
        elif c == ',' and bracket == 0:
            return i
    return -1

# 解析 count
comma1 = find_top_level_comma(line)
count = int(line[:comma1].strip())

# 解析 total
rest1 = line[comma1 + 1:].strip()
comma2 = find_top_level_comma(rest1)
total = int(rest1[:comma2].strip())

# 解析数组部分
rest2 = rest1[comma2 + 1:].strip()
split = rest2.find('],[')
values_str = rest2[:split + 1]
decays_str = '[' + rest2[split + 3:]

values = ast.literal_eval(values_str)
decays = ast.literal_eval(decays_str)

# 调用用户代码
print(Solution().maxMushroomValue(count, total, values, decays))
