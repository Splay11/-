import sys
import json

# 读取整行输入（整行即 JSON 字符串数组）
line = sys.stdin.read().strip()
dates = json.loads(line)

# 调用用户代码
result = Solution().normalizeDates(dates)

# 按题面格式输出：["a","b",...]（无空格）
print("[" + ",".join('"%s"' % x for x in result) + "]")
