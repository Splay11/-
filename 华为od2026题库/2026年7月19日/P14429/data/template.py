import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：n,passengers
first_comma = line.find(',')
n = int(line[:first_comma].strip())

# 剩余部分本身就是合法 Python 字面量：[[起点,终点],...]
passengers = ast.literal_eval(line[first_comma + 1:])

# 调用用户代码
print(Solution().maxRideProfit(n, passengers))
