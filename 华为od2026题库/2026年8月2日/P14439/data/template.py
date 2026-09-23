import sys

# 读取整行输入：capacity,efficiency,scene
line = sys.stdin.read().strip()
parts = line.split(',')
capacity = float(parts[0].strip())
efficiency = float(parts[1].strip())
scene = int(parts[2].strip())

# 调用用户代码
print(Solution().calculateRange(capacity, efficiency, scene))
