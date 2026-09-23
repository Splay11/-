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
    duration = ast.literal_eval(parts[1])
    deadline = ast.literal_eval(parts[2])
    profit = ast.literal_eval(parts[3])
    return duration, deadline, profit


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
duration, deadline, profit = parse_line(line)
ans = Solution().maximumProfit(duration, deadline, profit)
print(ans)
