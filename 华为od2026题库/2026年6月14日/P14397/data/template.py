import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
s = ast.literal_eval(line.strip())
ans = Solution().processString(s)
print(f'"{ans}"')
