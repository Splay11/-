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


def format_answer(ans):
    if not ans:
        return "[]"
    inner = []
    for combo in ans:
        inner.append("[" + ",".join(str(x) for x in combo) + "]")
    return "[" + ",".join(inner) + "]"


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
parts = split_top_level_commas(line.strip())
n = int(parts[0].strip())
k = int(parts[1].strip())
weights = ast.literal_eval(parts[2])
conflicts = ast.literal_eval(parts[3])
ans = Solution().selectMaxWeightPolicies(n, k, weights, conflicts)
print(format_answer(ans))
