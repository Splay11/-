import ast
import sys

# 读取整行输入，形如：n,[[u,v],...],startA,[p1,p2,...]
line = sys.stdin.read().strip()

# 按最外层逗号切分为 4 段：n、edges、startA、patrolPath
parts = []
depth = 0
cur = []
for ch in line:
    if ch == '[':
        depth += 1
        cur.append(ch)
    elif ch == ']':
        depth -= 1
        cur.append(ch)
    elif ch == ',' and depth == 0:
        parts.append(''.join(cur))
        cur = []
    else:
        cur.append(ch)
parts.append(''.join(cur))

n = int(parts[0])
edges = ast.literal_eval(parts[1])
startA = int(parts[2])
patrol_path = ast.literal_eval(parts[3])

# 调用用户代码
print(Solution().minMeetRounds(n, edges, startA, patrol_path))
