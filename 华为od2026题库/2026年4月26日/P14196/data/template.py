import ast
import sys

# 读取整行输入，格式：n,[[start,end],[start,end],...]
line = sys.stdin.read().strip()

# 没有输入时直接结束
if line:
    first_comma = line.find(',')
    playerCount = int(line[:first_comma].strip())
    playerTimeRange = ast.literal_eval(line[first_comma + 1:].strip())

    # 调用用户代码
    print(Solution().MaxPlayers(playerCount, playerTimeRange))
