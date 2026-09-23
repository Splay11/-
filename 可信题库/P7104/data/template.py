import ast
import sys

raw = sys.stdin.read()
if raw.endswith('\n'):
    raw = raw[:-1]
lines = raw.split('\n') if raw else []
n = int(lines[0]) if lines else 0
ops = ast.literal_eval(lines[1]) if len(lines) > 1 else []
print(Solution().maxLinkLoad(n, ops))
