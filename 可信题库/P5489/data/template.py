import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
raw = raw.strip()
scores = json.loads(raw) if raw else []
ans = Solution().bestShotRecords(scores)
print("[" + str(ans[0]) + ", " + str(ans[1]) + "]")
