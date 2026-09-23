import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
if not raw.strip():
    raise SystemExit(0)
lines = raw.split("\n")
tray = json.loads(lines[0])
stamp = json.loads(lines[1]) if len(lines) > 1 else []
print(json.dumps(Solution().findStampPos(tray, stamp)))
