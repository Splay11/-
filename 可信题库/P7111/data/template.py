import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
loads = json.loads(lines[0])
cap = int(lines[1].strip())
print(Solution().countLiveWindows(loads, cap))
