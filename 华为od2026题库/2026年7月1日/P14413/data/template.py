import ast
import sys

# 读取整行输入，格式为 "[nums],target"
line = sys.stdin.read().strip()
# 找到顶层逗号（不在嵌套括号内的逗号）
bracket = 0
split_idx = -1
for i, c in enumerate(line):
    if c == '[':
        bracket += 1
    elif c == ']':
        bracket -= 1
    elif c == ',' and bracket == 0:
        split_idx = i
        break

nums = ast.literal_eval(line[:split_idx])
target = int(line[split_idx + 1:])

# 调用用户代码
result = Solution().threeSumWithParity(nums, target)
# 输出格式：[[a,b,c],[d,e,f]]，无空格
print(str(result).replace(" ", ""))
