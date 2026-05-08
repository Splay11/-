import ast
import json
import sys


def _normalize_guards(raw):
    out = []
    for item in raw:
        if isinstance(item, (list, tuple)):
            out.append([int(item[0]), int(item[1])])
        else:
            raise ValueError("guard must be pair")
    return out


line = sys.stdin.read()
if not line:
    raise SystemExit(0)
line = line.strip()
if not line:
    raise SystemExit(0)
comma = line.find(",")
if comma < 0:
    raise SystemExit(1)
n = int(line[:comma].strip())
rest = line[comma + 1 :].strip()
raw = ast.literal_eval(rest)
if not isinstance(raw, list):
    raise SystemExit(1)
guards = _normalize_guards(raw)
ans = Solution().countShortestPaths(n, guards)
print(json.dumps(ans, separators=(",", ":"), ensure_ascii=False))
