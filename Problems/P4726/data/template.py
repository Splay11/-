import ast
import sys


def split_grid_k(line: str):
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
    grid_s = line[: end + 1]
    tail = line[end + 1 :].strip()
    if not tail.startswith(","):
        raise SystemExit(1)
    k = int(tail[1:].strip())
    return ast.literal_eval(grid_s), k


line = sys.stdin.read()
if not line:
    raise SystemExit(0)
line = line.strip()
grid, max_diff = split_grid_k(line)
ans = Solution().countHikingPaths(grid, max_diff)
print(ans)
