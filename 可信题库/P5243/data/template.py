import ast
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 4:
    raise SystemExit(0)
n = int(lines[0].strip())
deps = ast.literal_eval(lines[1])
buildTime = ast.literal_eval(lines[2])
changed = ast.literal_eval(lines[3])
ans = Solution().minRebuildTime(n, deps, buildTime, changed)
print(ans)
