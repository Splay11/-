import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析 JSON 数组
nums = ast.literal_eval(line)

# 调用用户代码
res = Solution().sortArrayByParity(nums)

# 输出 JSON 数组
print(str(res).replace(" ", ""))
