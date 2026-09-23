import ast
import sys

text = sys.stdin.read().strip()
if not text:
    raise SystemExit(0)
blackChessPoses = ast.literal_eval(text)
ans = Solution().hasFiveInRow(blackChessPoses)
print('"' + ans + '"')
