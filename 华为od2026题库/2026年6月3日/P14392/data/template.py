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
    file_ids = ast.literal_eval(parts[0])
    parent_ids = ast.literal_eval(parts[1])
    target_id = int(parts[2].strip())
    return file_ids, parent_ids, target_id


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
file_ids, parent_ids, target_id = parse_line(line)
ans = Solution().getLoadedFileIds(file_ids, parent_ids, target_id)
print("[" + ",".join(str(x) for x in ans) + "]")
