import json
import sys

line = sys.stdin.read().strip()

# 输入格式: ["tree_levelorder","frm","to"]
arr = json.loads(line)
treeLevelOrder = arr[0]
frm = arr[1]
to = arr[2]

print(Solution().minJumps(treeLevelOrder, frm, to))
