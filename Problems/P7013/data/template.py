import json, sys
lines=[ln for ln in sys.stdin.read().split("\n") if ln.strip()!=""]
if len(lines)<2: raise SystemExit(0)
print(Solution().countNeedUpgrade(json.loads(lines[0]), int(lines[1].strip())))
