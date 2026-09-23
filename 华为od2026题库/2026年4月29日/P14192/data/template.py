import ast
import sys

line = sys.stdin.read().strip()
L = ast.literal_eval(line) if line else ""

print(Solution().countValidPatterns(L), end="")
