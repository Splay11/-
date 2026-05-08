import ast
import json
import sys


def parse_leading_string(s: str):
    i = 0
    while i < len(s) and s[i] in " \t":
        i += 1
    if i >= len(s) or s[i] != '"':
        raise ValueError("expected opening quote")
    i += 1
    out = []
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 1
            if i < len(s):
                out.append(s[i])
                i += 1
            continue
        if c == '"':
            i += 1
            break
        out.append(c)
        i += 1
    rest = s[i:].lstrip()
    return "".join(out), rest


def split_two_top_arrays(s: str):
    s = s.strip()
    if not s.startswith("["):
        raise ValueError("need [")
    depth = 0
    in_str = False
    esc = False
    for i, c in enumerate(s):
        if esc:
            esc = False
            continue
        if c == "\\" and in_str:
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                first = s[: i + 1]
                j = i + 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                if j >= len(s) or s[j] != ",":
                    raise ValueError("comma between arrays")
                j += 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                return first, s[j:]
    raise ValueError("unclosed array")


line = sys.stdin.read()
if not line:
    raise SystemExit(0)
line = line.strip()
target, rest = parse_leading_string(line)
if not rest.startswith(","):
    raise SystemExit(1)
rest = rest[1:].strip()
files_str, sizes_str = split_two_top_arrays(rest)
files = ast.literal_eval(files_str)
sizes = ast.literal_eval(sizes_str)
ans = Solution().findMaxOccupiedPaths(target, files, sizes)
print(json.dumps(ans, ensure_ascii=False))
