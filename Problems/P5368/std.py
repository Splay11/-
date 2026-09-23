def farthest_posts(grid):
    # 曼哈顿距离 |r1-r2|+|c1-c2| 等于 max( |(r+c)之差|, |(r-c)之差| )
    # 因此只要在过道上分别记下 r+c、r-c 的最小点和最大点，取较差更大的那一对
    inf = 10 ** 18
    min_s, max_s = inf, -inf
    min_d, max_d = inf, -inf
    ps = qs = pd = qd = None
    for i, row in enumerate(grid, 1):
        for j, ch in enumerate(row, 1):
            if ch != ".":
                continue
            s = i + j
            d = i - j
            # 严格更新，保证四个极值对应真实过道
            if s < min_s:
                min_s = s
                ps = (i, j)
            if s > max_s:
                max_s = s
                qs = (i, j)
            if d < min_d:
                min_d = d
                pd = (i, j)
            if d > max_d:
                max_d = d
                qd = (i, j)
    # 若所有过道 r+c 都相同，ps 会和 qs 重合，必须改用 r-c 那一对
    if ps != qs and max_s - min_s >= max_d - min_d:
        return ps[0], ps[1], qs[0], qs[1]
    return pd[0], pd[1], qd[0], qd[1]


def main():
    h, w = map(int, input().split())
    grid = []
    for _ in range(h):
        grid.append(input().strip())
    r1, c1, r2, c2 = farthest_posts(grid)
    print(r1, c1, r2, c2)


if __name__ == "__main__":
    main()
