import sys

# 读取整行输入
s = sys.stdin.readline().rstrip('\n').rstrip('\r')

# 调用用户代码
print(Solution().compress(s))
