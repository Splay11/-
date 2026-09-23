import sys
import re

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：提取所有整数（支持可选负号）
nums = [int(x) for x in re.findall(r'-?\d+', line)]

# 调用用户代码
print(Solution().countDistinctTags(nums))
