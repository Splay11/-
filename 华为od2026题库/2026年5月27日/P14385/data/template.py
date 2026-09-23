import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：students, votes
students, votes = ast.literal_eval('[' + line + ']')

# 调用用户代码，并按题面要求输出带双引号的字符串
print('"' + Solution().electMonitor(students, votes) + '"')
