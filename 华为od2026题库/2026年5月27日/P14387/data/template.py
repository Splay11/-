import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
line = line.strip("\r\n")
br = line.index("[")
head = line[:br].rstrip(",")
n, m, k = map(int, head.split(","))
demands = ast.literal_eval(line[br:])
print(Solution().maxChargingDemand(n, m, k, demands))
