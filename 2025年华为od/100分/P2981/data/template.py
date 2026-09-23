import ast
import sys


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
heights = ast.literal_eval(line.strip())
ans = Solution().maxSolarPanelArea(heights)
print(ans)
