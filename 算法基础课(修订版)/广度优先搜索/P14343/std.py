from collections import deque

# 初始化读取输入数据
def init():
    n, m = map(int, input().split())  # 读取行数和列数
    a = [list(map(int, input().split())) for _ in range(n)]  # 读取矩阵，表示小区与垃圾站位置
    return n, m, a

def solve(n, m, a):
    # 初始化一个与原矩阵相同大小的矩阵，用于存储每个点的距离
    b = [[0] * m for _ in range(n)]
    q = deque()

    # 初始化队列，将所有垃圾站(值为0)的位置加入队列
    for i in range(n):
        for j in range(m):
            if a[i][j] == 0:
                q.append((i, j, 0))  # (x坐标, y坐标, 当前距离)

    # 定义四个方向的移动
    dx = [0, 0, -1, 1]  # 左右
    dy = [1, -1, 0, 0]  # 上下

    # BFS 广度优先遍历更新距离
    while q:
        x, y, now = q.popleft()  # 当前点的坐标及距离
        for i in range(4):  # 遍历四个方向
            nx, ny = x + dx[i], y + dy[i]
            # 检查新点是否在边界内
            if nx < 0 or nx >= n or ny < 0 or ny >= m:
                continue
            # 如果该点已经被更新，则跳过
            if b[nx][ny] != 0:
                continue
            # 如果该点是障碍物(值为-1)，则跳过
            if a[nx][ny] == -1:
                continue
            # 更新距离矩阵
            b[nx][ny] = now + 1
            q.append((nx, ny, now + 1))  # 将新点加入队列

    # 计算所有小区到垃圾站的最短距离总和
    total_sum = 0
    for i in range(n):
        for j in range(m):
            if a[i][j] == 1:  # 只对小区(值为1)计算距离
                total_sum += b[i][j]

    print(total_sum)  # 输出结果

# 主函数
if __name__ == "__main__":
    n, m, a = init()
    solve(n, m, a)
