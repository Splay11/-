import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 3:
    raise SystemExit(0)
sens = json.loads(lines[0])
baseCost = int(lines[1].strip())
maxBatches = int(lines[2].strip())
print(Solution().minRotateCost(sens, baseCost, maxBatches))
