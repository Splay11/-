import ast
import json
import sys


def _parse_line(line: str):
    s = line.strip()
    if not s:
        raise SystemExit(0)
    modules, dependencies = ast.literal_eval("(" + s + ")")
    if not isinstance(modules, list) or not isinstance(dependencies, list):
        raise SystemExit(1)
    mods = [str(x) for x in modules]
    deps = []
    for row in dependencies:
        if not isinstance(row, (list, tuple)) or len(row) != 2:
            raise SystemExit(1)
        deps.append([str(row[0]), str(row[1])])
    return mods, deps


raw = sys.stdin.read()
if not raw.strip():
    raise SystemExit(0)
mods, deps = _parse_line(raw)
ans = Solution().allBuildOrders(mods, deps)
print(json.dumps(ans, separators=(",", ":"), ensure_ascii=False))
