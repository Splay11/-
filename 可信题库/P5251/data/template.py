import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if not lines:
    raise SystemExit(0)
users = json.loads(lines[0])
print(Solution().firstDuplicate(users))
