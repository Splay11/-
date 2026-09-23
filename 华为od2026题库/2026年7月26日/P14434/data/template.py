import sys
import re

line = sys.stdin.read().strip()

# 用正则提取所有双引号内的字符串
parts = re.findall(r'"([^"]*)"', line)
num, sourceDigits, targetDigits = parts

print('"' + Solution().convertNumber(num, sourceDigits, targetDigits) + '"')
