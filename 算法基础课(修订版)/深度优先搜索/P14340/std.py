import sys
sys.setrecursionlimit(10**6)

def dfs(node, parent):
    has_red = has_black = False  # 标记当前子树是否包含红色和黑色
    if colors[node] == 'R':
        has_red = True
    else:
        has_black = True
    
    for neighbor in adj[node]:
        if neighbor != parent:
            r, b = dfs(neighbor, node)
            if r : has_red = True
            if b : has_black = True

    # 如果当前子树既有红色又有黑色节点，则满足条件
    if has_red and has_black:
        result[0] += 1

    return has_red, has_black

# 读取输入
n = int(input())
colors = input().strip()
edges = [list(map(int, input().split())) for _ in range(n-1)]

# 构建邻接表
adj = [[] for _ in range(n)]
for u, v in edges:
    adj[u-1].append(v-1)
    adj[v-1].append(u-1)

result = [0]
dfs(0, -1)
print(result[0])
