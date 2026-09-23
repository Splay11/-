from collections import deque

# 定义方向向量，分别表示上、下、左、右四个方向
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def shortest_path(grid, m, n, x1, y1, x2, y2):
    # 检查起点和终点是否为墙
    if grid[x1][y1] == 1 or grid[x2][y2] == 1:
        return -1

    # 创建访问数组，初始化为未访问
    visited = [[False] * n for _ in range(m)]
    # 创建队列存储坐标及当前路径长度
    q = deque([((x1, y1), 0)])
    visited[x1][y1] = True

    while q:
        (x, y), steps = q.popleft()

        # 如果当前坐标是目标点，返回路径长度
        if (x, y) == (x2, y2):
            return steps

        # 尝试向四个方向移动
        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            # 检查新坐标是否在范围内，且是空白格子，且未被访问
            if 0 <= new_x < m and 0 <= new_y < n and grid[new_x][new_y] == 0 and not visited[new_x][new_y]:
                q.append(((new_x, new_y), steps + 1))
                visited[new_x][new_y] = True  # 标记为已访问

    # 如果队列为空仍未找到目标点，返回 -1
    return -1

def main():
    # 输入迷宫的行数和列数
    m, n = map(int, input().split())

    # 读取矩阵
    grid = []
    for i in range(m):
        row = list(map(int, input().split()))
        grid.append(row)

    # 输入起点和终点的坐标
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    # 调用 shortest_path 函数计算最短路径
    result = shortest_path(grid, m, n, x1, y1, x2, y2)

    # 输出结果
    print(result)

if __name__ == "__main__":
    main()
