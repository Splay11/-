import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
hits = json.loads(raw) if raw else []
print(Solution().minForceWindow(hits))
