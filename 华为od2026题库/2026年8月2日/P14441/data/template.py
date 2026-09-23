import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：k,m,w,[a1,a2,...]
# 格式: 5,3,2,[3,4,3,4]
firstComma = line.find(',')
k = int(line[:firstComma].strip())

rest1 = line[firstComma + 1:]
secondComma = rest1.find(',')
m = int(rest1[:secondComma].strip())

rest2 = rest1[secondComma + 1:]
thirdComma = rest2.find(',')
w = int(rest2[:thirdComma].strip())

rest3 = rest2[thirdComma + 1:]
a = ast.literal_eval(rest3.strip())

# 调用用户代码
print(Solution().minSkillSegments(k, m, w, a))
