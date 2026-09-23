import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
scores = json.loads(raw) if raw else []
print(Solution().bestCorrectedTotal(scores))
