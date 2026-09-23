import sys


raw = sys.stdin.read()
if raw.endswith("\n"):
    raw = raw[:-1]
s = raw.strip()
print(Solution().reviseMarks(s))
