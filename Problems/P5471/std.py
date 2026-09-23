def min_tour(m, lo, hi, dur):
    """
    状态压缩求最短巡回时长。
    客户编号 1..m-1，仓站为 0。mask 的第 (v-1) 位表示客户 v 是否已送达。
    dp[mask][u]：已送达集合为 mask、当前停在 u 时的最早到达时刻。
    """
    k = m - 1
    full = (1 << k) - 1
    inf = 10 ** 9
    dp = [[inf] * m for _ in range(1 << k)]
    # 时刻 0 停在仓站，还没送过任何客户
    dp[0][0] = 0
    for mask in range(1 << k):
        for u in range(m):
            now = dp[mask][u]
            if now >= inf:
                continue
            # 枚举下一个尚未送达的客户
            for v in range(1, m):
                bit = 1 << (v - 1)
                if mask & bit:
                    continue
                t = now + dur[u][v]
                # 早到必须等到可收货下界，等候计入总时长
                if t < lo[v]:
                    t = lo[v]
                # 迟到则这条转移非法
                if t > hi[v]:
                    continue
                nmask = mask | bit
                if t < dp[nmask][v]:
                    dp[nmask][v] = t
    ans = inf
    # 所有客户都送达后，从最后一站回到仓站
    for u in range(1, m):
        if dp[full][u] >= inf:
            continue
        t = dp[full][u] + dur[u][0]
        if t < lo[0]:
            t = lo[0]
        if t > hi[0]:
            continue
        if t < ans:
            ans = t
    return -1 if ans >= inf else ans


def main():
    m = int(input())
    lo = []
    hi = []
    for _ in range(m):
        a, b = map(int, input().split())
        lo.append(a)
        hi.append(b)
    dur = []
    for _ in range(m):
        dur.append(list(map(int, input().split())))
    print(min_tour(m, lo, hi, dur))


if __name__ == "__main__":
    main()
