import ast
import sys

text = sys.stdin.read().strip()
if not text:
    raise SystemExit(0)
raw = ast.literal_eval(text)
table = [Cell(r, c, s) for r, c, s in raw]
ans = Solution().transformTable(table)
print("[" + ",".join('"' + line.replace("\\", "\\\\").replace('"', '\\"') + '"' for line in ans) + "]")
