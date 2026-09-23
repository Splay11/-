import sys
import json


# 读取 JSON 格式的二维数组输入
data = json.loads(sys.stdin.read().strip())

# 调用用户代码
res = Solution().countMinefields(data)

# 输出结果
print(res)
