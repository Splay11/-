import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if not lines:
    raise SystemExit(0)
starts = json.loads(lines[0])
ends = json.loads(lines[1])
print(Solution().peakConcurrent(starts, ends))
