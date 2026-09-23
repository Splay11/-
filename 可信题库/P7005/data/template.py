import json
import sys


text = sys.stdin.read().strip()
if not text:
    raise SystemExit(0)
loads = json.loads(text.split("\n")[0])
print(Solution().sumPeakRisk(loads))
