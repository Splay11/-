# 把非 0 格子当成城市，用状压 DP 求从中心出发并返回的最短回路


def min_steps(grid):
    n = len(grid)
    m = len(grid[0])
    sr = n // 2
    sc = m // 2
    # 点 0 固定为中心，其余点为中心以外的非 0 格子
    pts = [(sr, sc)]
    for i in range(n):
        for j in range(m):
            if grid[i][j] != 0 and (i != sr or j != sc):
                pts.append((i, j))
    k = len(pts)
    # 没有其它必访点时，已经在中心，步数为 0
    if k == 1:
        return 0

    def dist(a, b):
        return abs(pts[a][0] - pts[b][0]) + abs(pts[a][1] - pts[b][1])

    inf = 10**9
    full = 1 << k
    # dp[mask][i]：已访问集合为 mask、当前停在 i 的最少步数
    dp = [[inf] * k for _ in range(full)]
    dp[1][0] = 0
    for mask in range(full):
        for i in range(k):
            if (mask >> i) & 1 == 0 or dp[mask][i] >= inf:
                continue
            for j in range(k):
                if (mask >> j) & 1:
                    continue
                nxt = mask | (1 << j)
                cand = dp[mask][i] + dist(i, j)
                if cand < dp[nxt][j]:
                    dp[nxt][j] = cand
    end = full - 1
    ans = inf
    # 访问完全部点后，还要走回中心
    for i in range(k):
        cand = dp[end][i] + dist(i, 0)
        if cand < ans:
            ans = cand
    return ans


def main():
    n, m = map(int, input().split())
    grid = []
    for _ in range(n):
        grid.append(list(map(int, input().split())))
    print(min_steps(grid))


if __name__ == "__main__":
    main()
