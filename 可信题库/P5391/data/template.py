import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
desks = json.loads(raw) if raw else []
ans = Solution().canPassBooks(desks)
print("true" if ans else "false")
