import sys
import ast

# 读取整行输入并解析为 (n, m, files, cost)
line = sys.stdin.read().strip()
n, m, files, cost = ast.literal_eval(line)

# 调用用户代码
print(Solution().minCost(n, m, files, cost))
