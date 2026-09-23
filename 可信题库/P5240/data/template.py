import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 3:
    raise SystemExit(0)
events = json.loads(lines[0])
window = int(lines[1].strip())
limit = int(lines[2].strip())
print(Solution().countKeptAlarms(events, window, limit))
