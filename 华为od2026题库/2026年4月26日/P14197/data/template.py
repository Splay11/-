import ast
import sys

# 读取整行输入，格式如：[730,740,750,710,690,720,760,730]
line = sys.stdin.read().strip()

# 解析端口流量速率数组
portRates = ast.literal_eval(line)

# 调用用户代码
ans = Solution().StatPortRates(portRates)

# 按照题目要求输出，逗号后不加空格
print("[" + ",".join(map(str, ans)) + "]")
