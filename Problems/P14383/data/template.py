import ast
import sys


def parse_line(line: str):
    line = line.strip("\r\n")
    d = 0
    end = -1
    for i, c in enumerate(line):
        if c == "[":
            d += 1
        elif c == "]":
            d -= 1
            if d == 0:
                end = i
                break
    if end < 0:
        raise SystemExit(1)
    arr = ast.literal_eval(line[: end + 1])
    tail = line[end + 1 :].strip()
    if not tail.startswith(","):
        raise SystemExit(1)
    k = int(tail[1:].strip())
    return arr, k


line = sys.stdin.read()
if not line:
    raise SystemExit(0)
timestamps, min_interval = parse_line(line)
print(Solution().countValidPlans(timestamps, min_interval))
