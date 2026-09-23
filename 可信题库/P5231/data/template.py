import ast
import sys


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
section_width = ast.literal_eval(lines[0])
section_values = ast.literal_eval(lines[1])
ans = Solution().packFields(section_width, section_values)
print('"' + ans + '"')
