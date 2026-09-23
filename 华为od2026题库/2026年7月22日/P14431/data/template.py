import ast
import sys

# 读取整行输入并解析为整型数组
line = sys.stdin.read().strip()
nums = list(map(int, ast.literal_eval(line)))

# 调用用户代码
print(Solution().longestSubarray(nums))
