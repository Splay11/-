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
    resource_count = ast.literal_eval(parts[0])
    conflicts = []
    for p in parts[1:]:
        group = ast.literal_eval(p) if p else []
        conflicts.append([[int(a), int(b)] for a, b in group])
    return resource_count, conflicts


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
resource_count, conflicts = parse_line(line)
ans = Solution().canIsolateWithTwoPools(resource_count, conflicts)
print("[" + ",".join(str(x) for x in ans) + "]")
