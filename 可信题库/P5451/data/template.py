import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
raw = raw.strip()
pieces = json.loads(raw) if raw else []
print(Solution().minShareOps(pieces))
