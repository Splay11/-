import json
import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
raw = raw.strip()
note = json.loads(raw) if raw else ""
print(Solution().firstTasteLevel(note))
