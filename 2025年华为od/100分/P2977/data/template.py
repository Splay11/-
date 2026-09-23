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
    cap = int(parts[1].strip())
    workers = int(parts[2].strip())
    submit = ast.literal_eval(parts[3].strip())
    exec_times = ast.literal_eval(parts[4].strip())
    return submit, exec_times, cap, workers


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
submit, exec_times, cap, workers = parse_line(line)
ans = Solution().simulateTaskQueue(submit, exec_times, cap, workers)
print("[" + ",".join(str(x) for x in ans) + "]")
