def solve(n, k, S, R):
    for M in range(1, 7):
        # 检查保留部分范围
        if not (n - k <= R <= (n - k) * M):
            continue
        # 检查召回部分范围
        if not (k * M <= S - R <= k * 6):
            continue

        # 构造保留部分：n-k 个 ∈ [1, M]，和为 R
        retained = []
        extra = R - (n - k)          # 超出全 1 的部分
        for _ in range(n - k):
            add = extra if extra <= M - 1 else M - 1
            retained.append(1 + add)
            extra -= add

        # 构造召回部分：k 个 ∈ [M, 6]，和为 S-R
        removed = []
        extra = (S - R) - k * M       # 超出全 M 的部分
        for _ in range(k):
            add = extra if extra <= 6 - M else 6 - M
            removed.append(M + add)
            extra -= add

        return retained + removed
    return None


def main():
    n, k, S, R = map(int, input().split())
    ans = solve(n, k, S, R)
    if ans is None:
        print(-1)
    else:
        print(' '.join(map(str, ans)))


if __name__ == '__main__':
    main()
