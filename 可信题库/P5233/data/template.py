import ast
import sys

text = sys.stdin.read().strip()
if not text:
    raise SystemExit(0)
uriReqs = ast.literal_eval(text)
print(Solution().countSimilarGroups(uriReqs))
