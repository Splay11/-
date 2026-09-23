from collections import deque

def solve(n, k, m, x, y):
    # 初始化最短路径数组
    dist = [-1] * n
    dist[0] = 0  # 初始位置为0，0需要0次操作

    # BFS 队列
    q = deque([0])  # 从偏移量 0 开始

    while q:
        curr = q.popleft()

        for xi in x:
            next_offset = (curr + xi) % n  # 新的偏移量
            if dist[next_offset] == -1:  # 如果这个偏移量没有被访问过
                dist[next_offset] = dist[curr] + 1
                q.append(next_offset)

    # 输出每个查询的结果
    for target in y:
        print(dist[target])

# 手动输入部分
n, k, m = map(int, input().split())  # 读取 n, k, m
x = list(map(int, input().split()))  # 读取 k 个旋转操作
y = list(map(int, input().split()))  # 读取 m 个查询

solve(n, k, m, x, y)
