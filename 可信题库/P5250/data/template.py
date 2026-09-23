import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if not lines:
    raise SystemExit(0)
beats = json.loads(lines[0])
print(Solution().longestHealthy(beats))
