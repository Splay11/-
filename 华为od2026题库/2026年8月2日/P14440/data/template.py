import ast
import sys

# 读取整行输入（JSON 字符串列表）
line = sys.stdin.read().strip()

# 解析 JSON 数组
versions = ast.literal_eval(line)

# 调用用户代码
print('"' + Solution().findLatestVersion(versions) + '"')
