from collections import deque

def bfs_maze(maze, start, end, n, m):
    # 定义四个移动方向：上、下、左、右
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    # 初始化访问数组，所有位置初始为未访问
    visited = [[False] * m for _ in range(n)]

    # 使用队列进行 BFS
    q = deque()
    x1, y1 = start
    x2, y2 = end

    # 起点入队，并标记为已访问
    q.append((x1, y1))
    visited[x1][y1] = True

    while q:
        x, y = q.popleft()

        # 如果当前点是终点，返回 True
        if (x, y) == (x2, y2):
            return True
        
        # 尝试四个方向移动
        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            # 检查新位置是否在迷宫范围内，且是通路，且未被访问过
            if 0 <= new_x < n and 0 <= new_y < m and \
               maze[new_x][new_y] == 0 and not visited[new_x][new_y]:
                q.append((new_x, new_y))  # 将新节点加入队列
                visited[new_x][new_y] = True  # 标记为已访问

    return False

def main():
    # 输入迷宫的行数和列数
    n, m = map(int, input().split())

    # 输入迷宫地图
    maze = [list(map(int, input().split())) for _ in range(n)]

    # 输入起点和终点的坐标
    x1, y1, x2, y2 = map(int, input().split())

    # 检查起点和终点是否有效
    if maze[x1][y1] == 1 or maze[x2][y2] == 1:
        print("NO")
        return

    # 调用 BFS 检查是否能找到路径
    if bfs_maze(maze, (x1, y1), (x2, y2), n, m):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
