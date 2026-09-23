# 定义全局变量
countPaths = 0  # 记录路径数

# 四个方向：上，下，左，右
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 递归函数，当前坐标 (x, y)，已经走的步数 steps
def dfs(x, y, steps, n, sx, sy, ex, ey, k):
    global countPaths
    
    # 如果当前坐标是终点，则计数加一
    if x == ex and y == ey:
        countPaths += 1
    
    # 如果已经达到最大步数，停止递归
    if steps == k:
        return
    
    # 尝试四个方向移动
    for dir in range(4):
        newX = x + dx[dir]
        newY = y + dy[dir]
        # 检查新位置是否在网格内
        if 1 <= newX <= n and 1 <= newY <= n:
            dfs(newX, newY, steps + 1, n, sx, sy, ex, ey, k)

# 主函数
if __name__ == "__main__":
    # 输入
    n = int(input())  # 网格大小
    sx, sy, ex, ey = map(int, input().split())  # 起点和终点 (sx, sy, ex, ey)
    k = int(input())  # 最大步数
    
    # 开始递归，初始步数为 0
    dfs(sx, sy, 0, n, sx, sy, ex, ey, k)
    
    # 输出结果
    print(countPaths)
