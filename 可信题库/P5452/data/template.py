import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
raw = raw.strip()
weights = json.loads(raw) if raw else []
print(Solution().minCircleMerge(weights))
