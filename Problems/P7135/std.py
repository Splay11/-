def solve(grid1, grid2):
    """统计 grid2 里有多少座岛，整座岛的格子在 grid1 里也都是陆地。
    用栈做 DFS，m、n 到 500，蛇形岛递归会爆。
    """
    m = len(grid2)
    n = len(grid2[0])
    # 复制一份再染色，避免改到调用方的原矩阵
    g2 = [row[:] for row in grid2]
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def flood(si, sj):
        # 从 (si,sj) 出发把这座 grid2 岛走完，途中看 grid1 是否全是陆地
        ok = True
        stack = [(si, sj)]
        g2[si][sj] = 0
        while stack:
            i, j = stack.pop()
            if grid1[i][j] == 0:
                # 这座岛有一块在 grid1 里是水，就不能算子岛屿
                ok = False
            for di, dj in dirs:
                ni = i + di
                nj = j + dj
                if 0 <= ni < m and 0 <= nj < n and g2[ni][nj] == 1:
                    g2[ni][nj] = 0
                    stack.append((ni, nj))
        return ok

    ans = 0
    for i in range(m):
        for j in range(n):
            if g2[i][j] == 1:
                if flood(i, j):
                    ans += 1
    return ans


def main():
    # 第一行：行数 m、列数 n
    m, n = map(int, input().split())
    grid1 = []
    for _ in range(m):
        grid1.append(list(map(int, input().split())))
    grid2 = []
    for _ in range(m):
        grid2.append(list(map(int, input().split())))
    print(solve(grid1, grid2))


if __name__ == "__main__":
    main()
