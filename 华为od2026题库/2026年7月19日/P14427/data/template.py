import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 去掉字符串两端的引号
if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
    record = line[1:-1]
else:
    record = line

# 调用用户代码
res = Solution().findRepeatedServiceTypes(record)

# 按 [r,g,m] 格式输出
print('[' + ','.join(res) + ']')
