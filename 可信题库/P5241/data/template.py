import ast
import sys


def fmt_list(a):
    if not a:
        return "[]"
    return "[" + ", ".join(str(x) for x in a) + "]"


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 3:
    raise SystemExit(0)
arrival = ast.literal_eval(lines[0])
duration = ast.literal_eval(lines[1])
priority = ast.literal_eval(lines[2])
print(fmt_list(Solution().finishTimes(arrival, duration, priority)))
