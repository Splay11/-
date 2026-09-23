import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
intervals = ast.literal_eval(line.strip())
ans = Solution().countIsolatedIntervals(intervals)
print(ans)
