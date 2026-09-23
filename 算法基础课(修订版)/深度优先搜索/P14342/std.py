n, k = map(int, input().split())
vis = [[False] * n for _ in range(n)]

for _ in range(k):
    x, y = map(int, input().split())
    vis[x][y] = True

# 深度优先搜索
def dfs(x, y):
    if x >= n-1:  # 递归边界：到达最后一行
        return 0

    # 计算下一个搜索位置
    next_x, next_y = (x + 1, 0) if y == n - 2 else (x, y + 1)

    res = 0

    # 判断是否能放置2x2方块
    if x + 1 < n and y + 1 < n and not vis[x][y] and not vis[x + 1][y] and not vis[x][y + 1] and not vis[x + 1][y + 1]:
        # 标记格子为已访问
        vis[x][y] = vis[x + 1][y] = vis[x][y + 1] = vis[x + 1][y + 1] = True

        res = max(res, dfs(next_x, next_y) + 1)  # 递归继续搜索

        # 回溯，重置访问状态
        vis[x][y] = vis[x + 1][y] = vis[x][y + 1] = vis[x + 1][y + 1] = False

    # 不放置方块，继续搜索
    res = max(res, dfs(next_x, next_y))

    return res

print(dfs(0, 0))  # 从 (0, 0) 开始搜索
