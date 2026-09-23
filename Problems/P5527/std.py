from collections import deque


def shortest(grid):
    """网格 BFS 最短路，0 可走，1 墙。"""
    n = len(grid)
    m = len(grid[0])
    if grid[0][0] == 1 or grid[n - 1][m - 1] == 1:
        return -1
    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        x, y = q.popleft()
        if x == n - 1 and y == m - 1:
            return dist[x][y]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return -1


def main():
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    print(shortest(grid))


if __name__ == "__main__":
    main()
