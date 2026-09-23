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


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
parts = split_top_level_commas(line.strip())
loads = ast.literal_eval(parts[0])
edges = ast.literal_eval(parts[1])
ans = Solution().maxZoneImbalance(loads, edges)
print(ans)
