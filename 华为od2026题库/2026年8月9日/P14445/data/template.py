import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：priceRecords, hours, priceArray
first_comma = line.find(',')
priceRecords = int(line[:first_comma])

rest = line[first_comma + 1:]
second_comma = rest.find(',')
hours = int(rest[:second_comma])

# 解析数组 [a,b,c,...]
arr_str = rest[second_comma + 1:]
priceArray = ast.literal_eval(arr_str)

# 调用用户代码
print(Solution().findBestChargingTime(priceRecords, hours, priceArray))
