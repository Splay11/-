import ast
import sys


def fmt_list(a):
    if not a:
        return "[]"
    return "[" + ", ".join(str(x) for x in a) + "]"


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
rects = ast.literal_eval(lines[0])
query = ast.literal_eval(lines[1])
ans = Solution().queryVisibleRects(rects, query)
print(fmt_list(ans))
