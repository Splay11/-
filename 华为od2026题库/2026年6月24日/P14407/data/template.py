import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
commands = ast.literal_eval(line.strip())
ans = Solution().queryNetEnergy(commands)
print(ans)
