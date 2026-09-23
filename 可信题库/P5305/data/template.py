import json,sys
lines=[ln for ln in sys.stdin.read().split('\n') if ln.strip()!='']
if not lines: raise SystemExit(0)
print(Solution().maxMaintenanceScore(json.loads(lines[0])))
