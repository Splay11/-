import ast
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 4:
    raise SystemExit(0)
load = ast.literal_eval(lines[0])
runCost = int(lines[1].strip())
changeCost = int(lines[2].strip())
maxChanges = int(lines[3].strip())
ans = Solution().minComputeCost(load, runCost, changeCost, maxChanges)
print(ans)
