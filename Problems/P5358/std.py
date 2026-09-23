from collections import deque


def shortest(h, w, a):
    # 起点或终点是货架，直接到不了
    if a[0][0] == 1 or a[h - 1][w - 1] == 1:
        return -1
    # dist[i][j] 表示走到 (i,j) 时已经踩过的格子数；0 表示还没访问
    dist = [[0] * w for _ in range(h)]
    q = deque()
    dist[0][0] = 1
    q.append((0, 0))
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while q:
        x, y = q.popleft()
        if x == h - 1 and y == w - 1:
            return dist[x][y]
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            # 越界、货架、已经走过的格子都跳过
            if nx < 0 or nx >= h or ny < 0 or ny >= w:
                continue
            if a[nx][ny] == 1 or dist[nx][ny] != 0:
                continue
            dist[nx][ny] = dist[x][y] + 1
            q.append((nx, ny))
    return -1


def main():
    parts = input().split()
    h = int(parts[0])
    w = int(parts[1])
    a = []
    for _ in range(h):
        a.append(list(map(int, input().split())))
    print(shortest(h, w, a))


if __name__ == "__main__":
    main()
