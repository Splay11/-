import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：N,[已交卷学号列表]
comma = line.find(',')
n = int(line[:comma].strip())
submitted = ast.literal_eval(line[comma + 1:])  # 形如 [1,5,3,...]

# 调用用户代码
result = Solution().findMissingStudents(n, submitted)

# 按题面格式输出：[a,b,c]（无空格）
print("[" + ",".join(str(x) for x in result) + "]")
