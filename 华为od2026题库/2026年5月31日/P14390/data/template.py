
import ast
import sys

# 读取整份输入
line = sys.stdin.read().strip()

# 没有输入则退出
if not line:
    sys.exit(0)

# 把 LeetCode 风格输入包装成 Python 元组解析
# 支持两种格式：
# 1. [1,2,3],3
# 2. [1,2,3],3,5
data = ast.literal_eval("(" + line + ")")

# 如果只有 nums 和 k，则 n 自动等于 len(nums)
if len(data) == 2:
    nums, k = data
    n = len(nums)
else:
    nums, n, k = data

# 调用用户提交的 Solution 方法
print(Solution().maxEnergyDivisibleByK(nums, n, k))
