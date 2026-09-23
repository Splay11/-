import json
import sys

line = sys.stdin.read().strip()

# 按顶层括号深度找逗号，将输入切分为三个 JSON 数组
depth = 0
splits = []
for i, c in enumerate(line):
    if c == '[':
        depth += 1
    elif c == ']':
        depth -= 1
    elif c == ',' and depth == 0:
        splits.append(i)

green = json.loads(line[:splits[0]])
carbon = json.loads(line[splits[0] + 1:splits[1]])
edges = json.loads(line[splits[1] + 1:])

result = Solution().maxCarbonReduction(green, carbon, edges)
print(result)
