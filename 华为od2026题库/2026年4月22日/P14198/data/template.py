import ast
import sys

line = sys.stdin.read().strip()
data = ast.literal_eval('[' + line + ']')
names, ballotTickets = data

ans = Solution().getClassMonitor(names, ballotTickets)
print('"' + ans.replace('\\', '\\\\').replace('"', '\\"') + '"')
