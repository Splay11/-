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
    temperatures = ast.literal_eval(parts[1].strip())
    k = int(parts[2].strip())
    t = int(parts[3].strip())
    return temperatures, k, t


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
temperatures, k, t = parse_line(line)
ans = Solution().analyzeTemperatureData(temperatures, k, t)
print("[" + ",".join(str(x) for x in ans) + "]")
