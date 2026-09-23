# 把业务条目映射成二进制，每台机器变成覆盖掩码，再做 0-1 最短覆盖 DP


def min_devices(specs, need):
    """
    specs[i] 是第 i 台机器的条目列表，need 是业务点名的互异条目。
    返回最少启用台数；凑不齐返回 0。
    """
    # 只关心业务点名的条目，给它们编号 0..t-1
    bit = {}
    for i, x in enumerate(need):
        bit[x] = i
    t = len(need)
    covers = []
    for row in specs:
        mask = 0
        for x in row:
            if x in bit:
                mask |= 1 << bit[x]
        covers.append(mask)
    full = (1 << t) - 1
    inf = t + 5
    # dp[s]：覆盖集合恰好为 s 时的最少台数
    dp = [inf] * (1 << t)
    dp[0] = 0
    for c in covers:
        if c == 0:
            continue
        # 倒序枚举，保证每台机器最多用一次
        for s in range((1 << t) - 1, -1, -1):
            if dp[s] >= inf:
                continue
            ns = s | c
            v = dp[s] + 1
            if v < dp[ns]:
                dp[ns] = v
    ans = dp[full]
    return 0 if ans >= inf else ans


def main():
    d, w, t = map(int, input().split())
    specs = []
    for _ in range(d):
        specs.append(list(map(int, input().split())))
    need = list(map(int, input().split()))
    print(min_devices(specs, need))


if __name__ == "__main__":
    main()
