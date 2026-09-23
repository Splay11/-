import ast
import sys

# 读取整行输入，格式为 "[a1,a2,...,an]"
line = sys.stdin.read().strip()
items = ast.literal_eval(line)

# 调用用户代码
result = Solution().warehouseInventory(items)
# 输出格式要求：[x1,x2,...] 无空格
print('[' + ','.join(str(x) for x in result) + ']')
