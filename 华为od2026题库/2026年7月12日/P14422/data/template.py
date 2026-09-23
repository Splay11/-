import ast
import sys

# 读取整行输入（单行二维数组 [[priority, weight], ...]）
line = sys.stdin.readline().rstrip('\n').rstrip('\r')

# 解析二维整型数组
packets = ast.literal_eval(line)

# 调用用户代码
res = Solution().findPacket(packets)

# 按题面样例格式输出：[id1,id2,...]（无空格）
print("[" + ",".join(str(x) for x in res) + "]")
