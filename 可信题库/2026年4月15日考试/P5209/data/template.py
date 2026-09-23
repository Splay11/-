import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
numbers = ast.literal_eval(line.strip("\r\n"))
print(Solution().sumOfSubarrayMedians(numbers))
