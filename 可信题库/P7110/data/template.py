import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
slots = json.loads(lines[0])
prep = json.loads(lines[1])
print(Solution().minPassDays(slots, prep))
