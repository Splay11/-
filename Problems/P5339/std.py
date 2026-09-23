from collections import deque


def count_closed(grid):
    h = len(grid)
    w = len(grid[0])
    vis = [[False] * w for _ in range(h)]
    q = deque()

    # 从边界上的村庄出发，能走到的都是自由村庄
    def add(i, j):
        if i < 0 or i >= h or j < 0 or j >= w:
            return
        if grid[i][j] != "V" or vis[i][j]:
            return
        vis[i][j] = True
        q.append((i, j))

    for j in range(w):
        add(0, j)
        add(h - 1, j)
    for i in range(h):
        add(i, 0)
        add(i, w - 1)

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            add(i + di, j + dj)

    ans = 0
    for i in range(h):
        for j in range(w):
            # 没被边界搜到的村庄就是封闭领地
            if grid[i][j] == "V" and not vis[i][j]:
                ans += 1
    return ans


def main():
    h, w = map(int, input().split())
    grid = []
    for _ in range(h):
        grid.append(input().strip())
    print(count_closed(grid))


if __name__ == "__main__":
    main()
