import ast
import sys

line = sys.stdin.read().strip()
s, n = ast.literal_eval("(" + line + ")")
ans = Solution().processChunks(s, n)
print(f'"{ans}"')
