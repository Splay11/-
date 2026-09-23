import ast
import sys


def split_top_level_commas(s: str):
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(s):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts


def parse_line(line: str):
    line = line.strip("\r\n")
    parts = split_top_level_commas(line)
    n = int(parts[0].strip())
    w = int(parts[1].strip())
    scores = ast.literal_eval(parts[2].strip())
    return n, w, scores


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
n, w, scores = parse_line(line)
ans = Solution().findMaintenanceWindow(n, w, scores)
print("[" + ",".join(str(x) for x in ans) + "]")
