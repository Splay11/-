import ast
import sys


def fmt_list(a):
    return "[" + ",".join(str(x) for x in a) + "]"


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
numbers = ast.literal_eval(line.strip("\r\n"))
ans = Solution().sortOddEven(numbers)
print(fmt_list(ans))
