def dfs(node, father):
    traversal_result.append(node)  # 先访问当前节点
    for child in adjList[node]:
        if child != father:  # 避免回到父节点
            dfs(child, node)  # 递归访问子节点


# 主程序
n = int(input())  # 读取节点数
tree_type = int(input())  # 读取表示方式

adjList = [[] for _ in range(n + 1)]  # 邻接表
traversal_result = []  # 存储遍历结果

if tree_type == 1:
    # 方式一：通过边的形式输入
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adjList[u].append(v)  # 添加子节点
        adjList[v].append(u)  # 添加父节点（无向树）
elif tree_type == 2:
    # 方式二：通过father数组输入
    father = list(map(int, input().split()))
    for i in range(1, n + 1):
        if father[i-1] != 0:
            adjList[father[i-1]].append(i)  # 添加子节点
            #adjList[i].append(father[i-1])  # 添加父节点

# 为了保证遍历顺序的一致性，先对每个节点的子节点进行排序
for i in range(1, n + 1):
    adjList[i].sort()

# 执行dfs，根节点为1，父节点为0（无）
dfs(1, 0)

# 输出遍历结果
print(" ".join(map(str, traversal_result)))
