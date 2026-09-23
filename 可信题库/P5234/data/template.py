import ast
import sys

text = sys.stdin.read().strip()
if not text:
    raise SystemExit(0)
lettersStr = ast.literal_eval(text)
ans = Solution().sortLetter(lettersStr)
print('"' + ans + '"')
