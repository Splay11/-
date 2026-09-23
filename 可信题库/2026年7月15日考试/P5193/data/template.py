import ast
import sys


lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
charMatrix = ast.literal_eval(lines[0])
words = ast.literal_eval(lines[1])
print(Solution().countMatchedWords(charMatrix, words))
