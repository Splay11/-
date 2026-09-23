import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入："lights",t
# 格式: "RRRRRRRRRRRRRRRR",1
# 找到第一个引号后的内容，直到下一个引号
start = line.find('"')
end = line.find('"', start + 1)
lights = line[start + 1:end]

# 逗号后的整数
comma = line.find(',', end)
t = int(line[comma + 1:].strip())

# 调用用户代码
result = Solution().lightStripTransform(lights, t)
# 输出带引号的结果
print('"' + result + '"')
