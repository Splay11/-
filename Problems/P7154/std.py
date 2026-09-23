def solve(grid):
    """dp[i][j] 表示走到 (i,j) 的最小路径和。
    第一行只能从左边走来，第一列只能从上边走来，其余格子取上、左的较小值再加当前格。
    """
    m = len(grid)
    n = len(grid[0])
    dp = [row[:] for row in grid]
    # 第一列只能一直往下
    for i in range(1, m):
        dp[i][0] += dp[i - 1][0]
    # 第一行只能一直往右
    for j in range(1, n):
        dp[0][j] += dp[0][j - 1]
    for i in range(1, m):
        for j in range(1, n):
            # 只能从上或从左走来
            dp[i][j] += min(dp[i - 1][j], dp[i][j - 1])
    return dp[m - 1][n - 1]


def main():
    # 第一行 m n，接着 m 行每行 n 个数
    m, n = map(int, input().split())
    grid = []
    for _ in range(m):
        grid.append(list(map(int, input().split())))
    print(solve(grid))


if __name__ == "__main__":
    main()
