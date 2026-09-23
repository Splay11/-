import json
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if not lines:
    raise SystemExit(0)
n = int(lines[0])
prev = json.loads(lines[1])
next_arr = json.loads(lines[2])
time_arr = json.loads(lines[3])
print(Solution().minFinishTime(n, prev, next_arr, time_arr))
