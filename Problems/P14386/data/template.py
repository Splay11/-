import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
type_arr = ast.literal_eval(line.strip("\r\n"))
print(Solution().longestValidSkillChain(type_arr))
