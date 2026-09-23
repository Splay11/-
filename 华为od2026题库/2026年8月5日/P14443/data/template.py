import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：n,"channels"
first_comma = line.find(',')
n = int(line[:first_comma].strip())

# 提取引号内的字符串
rest = line[first_comma + 1:].strip()
channels = rest.strip('"')

# 调用用户代码
print(Solution().mergeBroadcastChannels(n, channels))
