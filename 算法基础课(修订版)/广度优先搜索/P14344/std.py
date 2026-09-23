from collections import deque

# 读取迷宫大小n和最大允许步数k
n = int(input())
k = int(input())

# 读取迷宫的辐射值矩阵a
a = [list(map(int, input().split())) for _ in range(n)]

def bfs(val):
    """
    广度优先搜索函数，检查是否可以在k步内从起点到达终点，
    且所有经过的格子的辐射值不超过val。
    """
    # 如果起点或终点的辐射值超过val，无法通过
    if a[0][0] > val or a[n-1][n-1] > val:
        return False
    
    # 初始化访问矩阵，记录是否访问过
    visited = [[False]*n for _ in range(n)]
    # 使用deque作为队列，存储当前坐标和步数
    q = deque([(0, 0, 0)])  # (x, y, steps)
    visited[0][0] = True  # 标记起点已访问
    
    # 定义四个可能的移动方向：右、下、左、上
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    
    while q:
        x, y, steps = q.popleft()  # 取出队首元素
        # 如果到达终点，检查步数是否在允许范围内
        if x == n-1 and y == n-1:
            return steps <= k
        # 遍历所有可能的移动方向
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # 计算新坐标
            # 检查新坐标是否在迷宫范围内
            if 0 <= nx < n and 0 <= ny < n:
                # 检查新位置的辐射值是否不超过val，且未被访问过
                if not visited[nx][ny] and a[nx][ny] <= val:
                    # 检查步数是否不会超过k
                    if steps + 1 > k:
                        continue
                    visited[nx][ny] = True  # 标记为已访问
                    q.append((nx, ny, steps + 1))  # 将新位置加入队列
    # 如果无法到达终点
    return False

# 确定二分查找的初始边界
left = max(a[0][0], a[n-1][n-1])  # 防护力的最低可能值
right = max(max(row) for row in a)  # 防护力的最高可能值

# 二分查找寻找最小的满足条件的防护力
while left <= right:
    mid = (left + right) // 2  # 取中间值作为当前防护力
    if bfs(mid):
        right = mid - 1  # 尝试更小的防护力
    else:
        left = mid + 1  # 增加防护力

# 输出最终结果
print(left)
