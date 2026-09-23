def main():
    n = int(input())
    d = [0] + list(map(int, input().split()))
    # dp[i][j]：中序区间 [i,j] 的最高加分；root[i][j]：最优根
    # 空树加分为 1；叶子加分等于自身分数
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 1):
        dp[i][i] = d[i]
        root[i][i] = i
        dp[i][i - 1] = 1  # 空区间
    dp[n + 1][n] = 1

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            best = -1
            best_r = i
            for k in range(i, j + 1):
                left = dp[i][k - 1] if k > i else 1
                right = dp[k + 1][j] if k < j else 1
                score = left * right + d[k]
                # 严格大于才更新，平分时保留更左的根
                if score > best:
                    best = score
                    best_r = k
            dp[i][j] = best
            root[i][j] = best_r

    def preorder(i, j, out):
        if i > j:
            return
        r = root[i][j]
        out.append(r)
        preorder(i, r - 1, out)
        preorder(r + 1, j, out)

    print(dp[1][n])
    seq = []
    preorder(1, n, seq)
    print(*seq)


if __name__ == "__main__":
    main()
