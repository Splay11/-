import ast
import sys


def parse_line(line: str):
    line = line.strip("\r\n")
    p1 = line.index(",")
    p2 = line.index(",", p1 + 1)
    n = int(line[:p1])
    m = int(line[p1 + 1 : p2])
    cars = ast.literal_eval(line[p2 + 1 :])
    return n, m, cars


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
n, m, cars = parse_line(line)
print(Solution().countFailedCharging(n, cars))
