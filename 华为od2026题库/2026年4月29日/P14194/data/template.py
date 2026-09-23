import ast
import sys

line = sys.stdin.read().strip()
logs = ast.literal_eval(line)

ans = Solution().findAnomalyLogs(logs)

if len(ans) == 0:
    print("NONE", end="")
else:
    print("[" + ",".join('"' + x + '"' for x in ans) + "]", end="")
