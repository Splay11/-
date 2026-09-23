import ast
import sys

line = sys.stdin.read().strip()
docs = ast.literal_eval(line)

print(Solution().featureExtraction(docs))
