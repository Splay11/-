MOD = 10**9 + 7
q = int(input())
for _ in range(q):
    m, d = map(int, input().split())
    h = list(map(int, input().split()))
    # 滚动维护前缀编组方案数
    dp0, dp1 = 1, 1
    for i in range(1, m):
        nd = dp1  # 第 i 人单独成组
        if h[i] - h[i - 1] <= d:
            nd = (nd + dp0) % MOD  # 与前一人配对
        dp0, dp1 = dp1, nd
    print(1 if m == 0 else dp1)
