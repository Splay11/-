import ast
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 5:
    raise SystemExit(0)
n = int(lines[0].strip())
edges = ast.literal_eval(lines[1])
src = int(lines[2].strip())
dst = int(lines[3].strip())
riskBudget = int(lines[4].strip())
print(Solution().minTrustDelay(n, edges, src, dst, riskBudget))
