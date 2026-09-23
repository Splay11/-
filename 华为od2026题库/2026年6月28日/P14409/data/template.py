import ast
import sys

line = sys.stdin.read().strip()
if not line:
    raise SystemExit(0)
first_comma = line.find(",")
if first_comma < 0:
    raise SystemExit(1)
n = int(line[:first_comma].strip())
nums = ast.literal_eval(line[first_comma + 1 :].strip())
if len(nums) != n:
    raise SystemExit(1)
print(Solution().minSplitRangeSum(nums))
