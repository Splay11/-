
import ast
import sys

# 读取 LeetCode 风格输入：["add","query"],[1,1]
line = sys.stdin.read().strip()
ops, vals = ast.literal_eval("[" + line + "]")

# 调用用户代码
ans = Solution().monitor(ops, vals)

# 输出 LeetCode 数组格式
print("[" + ",".join(str(x) for x in ans) + "]", end="")
