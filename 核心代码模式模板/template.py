import ast
import sys

# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入：month, employees, birthdays
first_comma = line.find(',')
month = int(line[:first_comma].strip())

rest = '[' + line[first_comma + 1:] + ']'
employees, birthdays = ast.literal_eval(rest)

# 调用用户代码
print(Solution().countBirthdayGifts(month, employees, birthdays))
