# -*- coding: utf-8 -*-
"""P5309 造数：水域四连通 BFS 到边界，带出口与路径和并列规则。"""
import os
import random
from collections import deque

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(r, c, sx, sy, a):
    if a[sx][sy] == 1:
        return None
    inf = 10 ** 9
    dist = [[inf] * c for _ in range(r)]
    rsum = [[0] * c for _ in range(r)]
    csum = [[0] * c for _ in range(r)]
    parent = [[None] * c for _ in range(r)]
    dist[sx][sy] = 0
    rsum[sx][sy] = sx
    csum[sx][sy] = sy
    q = deque([(sx, sy)])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= r or ny < 0 or ny >= c or a[nx][ny] != 0:
                continue
            nd = dist[x][y] + 1
            nrs = rsum[x][y] + nx
            ncs = csum[x][y] + ny
            if nd < dist[nx][ny]:
                dist[nx][ny] = nd
                rsum[nx][ny] = nrs
                csum[nx][ny] = ncs
                parent[nx][ny] = (x, y)
                q.append((nx, ny))
            elif nd == dist[nx][ny] and (nrs, ncs) < (rsum[nx][ny], csum[nx][ny]):
                rsum[nx][ny] = nrs
                csum[nx][ny] = ncs
                parent[nx][ny] = (x, y)
    best = None
    for i in range(r):
        for j in range(c):
            if dist[i][j] >= inf:
                continue
            if i == 0 or i == r - 1 or j == 0 or j == c - 1:
                cur = (dist[i][j], i, j)
                if best is None or cur < best:
                    best = cur
    if best is None:
        return None
    path = []
    cur = (best[1], best[2])
    while cur is not None:
        path.append(cur)
        cur = parent[cur[0]][cur[1]]
    path.reverse()
    return path


def fmt(path):
    if path is None:
        return "-1"
    lines = [str(len(path) - 1)]
    for x, y in path:
        lines.append("%d %d" % (x, y))
    return "\n".join(lines)


def write_case(idx, r, c, sx, sy, a):
    assert 3 <= r <= 20 and 3 <= c <= 30
    assert 0 <= sx < r and 0 <= sy < c
    for i in range(r):
        assert len(a[i]) == c
        for j in range(c):
            assert a[i][j] in (0, 1)
    path = solve(r, c, sx, sy, a)
    lines = ["%d %d" % (r, c), "%d %d" % (sx, sy)]
    for i in range(r):
        lines.append(" ".join(str(x) for x in a[i]))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(fmt(path) + "\n")


def main():
    rng = random.Random(5309)

    # 1 改写样例1：困住
    write_case(1, 3, 3, 1, 1, [[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    # 2 改写样例2：四个出口选行号最小
    write_case(2, 3, 3, 1, 1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # 3 起点陆地
    write_case(3, 3, 3, 0, 0, [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    # 4 起点已在边界水域
    write_case(4, 3, 3, 0, 1, [[1, 0, 1], [0, 0, 0], [1, 0, 1]])
    # 5 原题风格：有唯一出口
    write_case(
        5,
        4,
        5,
        1,
        1,
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1],
        ],
    )
    # 6 两条最短路同一出口，应选行号和更小的
    write_case(
        6,
        5,
        4,
        2,
        1,
        [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1],
        ],
    )
    # 7 多个出口同距离，选更小的终点坐标
    write_case(
        7,
        4,
        4,
        1,
        1,
        [
            [1, 0, 1, 1],
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [1, 1, 1, 1],
        ],
    )
    # 8 小随机：保证 0/1
    r, c = 6, 8
    a = [[rng.randint(0, 1) for _ in range(c)] for _ in range(r)]
    a[2][3] = 0
    write_case(8, r, c, 2, 3, a)
    # 9 满规模随机
    r, c = 20, 30
    a = [[rng.randint(0, 1) for _ in range(c)] for _ in range(r)]
    a[10][15] = 0
    write_case(9, r, c, 10, 15, a)
    # 10 满规模：内部水域连通到上边界，卡「随便搜到一个出口」
    r, c = 20, 30
    a = [[1] * c for _ in range(r)]
    for i in range(1, 19):
        a[i][10] = 0
    for j in range(10, 25):
        a[5][j] = 0
    a[0][10] = 0
    a[0][24] = 0
    write_case(10, r, c, 18, 10, a)

    for i in range(1, 11):
        with open(os.path.join(DIR, "%d.in" % i), "r", encoding="utf-8") as f:
            raw = f.read()
        assert not raw.endswith("\n"), "输入末尾多了换行: %d.in" % i
        lines = raw.split("\n")
        r, c = map(int, lines[0].split())
        sx, sy = map(int, lines[1].split())
        a = [list(map(int, lines[2 + k].split())) for k in range(r)]
        with open(os.path.join(DIR, "%d.out" % i), "r", encoding="utf-8") as f:
            out = f.read()
        assert out.endswith("\n") and out == fmt(solve(r, c, sx, sy, a)) + "\n"
    print("ok")


if __name__ == "__main__":
    main()
