import sys

# 读取单个整数 n
data = sys.stdin.read().strip()
if data:
    n = int(data)
    print(Solution().equalDistanceBinary(n))
