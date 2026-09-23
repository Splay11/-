from collections import deque

# 全局邻接表，假设节点编号从1到10000
adj = [[] for _ in range(10001)]
visited = [False] * 10001  # 访问标记列表

def bfs(start):
    queue = deque()
    queue.append(start)
    visited[start] = True  # 标记起始节点为已访问

    while queue:
        node = queue.popleft()
        # 遍历所有相邻节点
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True  # 标记为已访问
                queue.append(neighbor)    # 加入队列继续遍历

def main():
    import sys
    input = sys.stdin.readline  # 使用readline提高输入效率

    n, m = map(int, input().split())  # 读取节点数和边数

    # 读取边的信息并构建邻接表
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)  # 无向图双向连接

    count = 0  # 连通块数量

    # 遍历所有节点，进行BFS
    for i in range(1, n + 1):
        if not visited[i]:
            bfs(i)
            count += 1  # 每找到一个连通块，计数加1

    print(count)  # 输出连通块的数量

if __name__ == "__main__":
    main()
