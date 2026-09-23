import json,sys
lines=[ln for ln in sys.stdin.read().split('\n') if ln.strip()!='']
if len(lines)<3: raise SystemExit(0)
print(Solution().maxDropoffReach(int(lines[0]), json.loads(lines[1]), json.loads(lines[2])))
