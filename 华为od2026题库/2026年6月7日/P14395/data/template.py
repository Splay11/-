import ast
import sys


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
ips = ast.literal_eval(line.strip())
ans = Solution().filterValidAClassIPs(ips)
print("[" + ",".join(f'"{x}"' for x in ans) + "]")
