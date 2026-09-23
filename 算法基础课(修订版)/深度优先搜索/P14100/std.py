MAX = 1001  # 假设最大节点数为 1000
adj = [[] for _ in range(MAX)]  # 邻接表存储图
visited = [False] * (MAX)  # 访问标记数组

# DFS 函数（递归实现）
def dfs(node):
    visited[node] = True  # 标记当前节点为已访问
    for neighbor in adj[node]:  # 遍历该节点的邻居
        if not visited[neighbor]:  # 如果邻居未被访问
            dfs(neighbor)  # 递归访问邻居节点

def main():
    n, m = map(int, input().split())  # 读取节点数和边数

    # 初始化邻接表和访问标记数组
    for i in range(1, n + 1):
        visited[i] = False
        adj[i] = []

    # 读取边并构建邻接表
    for _ in range(m):
        u, v = map(int, input().split())
        if u != v:  # 忽略自环
            adj[u].append(v)
            adj[v].append(u)

    # 统计联通块数量
    count = 0
    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)  # 启动 DFS
            count += 1  # 每次启动 DFS，发现一个新的连通块

    print(count)

if __name__ == "__main__":
    main()
