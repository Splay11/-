import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：JSON 整数数组 [a1,a2,...]
nums = ast.literal_eval(line)

# 调用用户代码
print(Solution().longestNonConsecutiveSubstring(nums))
