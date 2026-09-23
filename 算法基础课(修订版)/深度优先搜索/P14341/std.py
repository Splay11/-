import sys
sys.setrecursionlimit(200000)

def dfs(node, father, adj, a):
    total_add = 0
    total_sum = 0  # 记录子树的总权值和
    
    # 处理所有子节点
    for neighbor in adj[node]:
        if neighbor != father:
            child_add, child_sum = dfs(neighbor, node, adj, a)
            total_add += child_add
            total_sum += child_sum
    
    # 确保当前节点的权值大于等于所有子节点的权值和
    if a[node] < total_sum:
        total_add += total_sum - a[node]
        a[node] = total_sum  # 将当前节点的权值增加到子节点权值和
    
    # 返回当前节点需要增加的操作次数和当前节点的总权值
    return total_add, a[node]

def solve(n, a, edges):
    # 构建树的邻接表
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    
    # 初始化
    result, _ = dfs(0, -1, adj, a)  # 从根节点0开始DFS
    return result

# 输入部分
n = int(input())  # 节点数
a = list(map(int, input().split()))  # 权值数组
edges = [tuple(map(int, input().split())) for _ in range(n-1)]  # 边的输入

# 调用函数并输出结果
print(solve(n, a, edges))
