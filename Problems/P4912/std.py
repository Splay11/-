# -*- coding: utf-8 -*-


def feasible(n, m, s, g):
    if g <= 0:
        return True
    gap = [s[i + 1] - s[i] for i in range(n - 1)]
    tot_bad = sum(1 for x in gap if x < g)
    pref_bad = [0] * (n - 1)
    for i in range(n - 1):
        pref_bad[i] = (pref_bad[i - 1] if i else 0) + (1 if gap[i] < g else 0)
    pref_max = gap[:]
    for i in range(1, n - 1):
        pref_max[i] = max(pref_max[i - 1], pref_max[i])
    suf_max = gap[:]
    for i in range(n - 3, -1, -1):
        suf_max[i] = max(suf_max[i], suf_max[i + 1])
    pref_large = [-1] * (n - 1)
    for i in range(n - 1):
        if gap[i] < g:
            pref_large[i] = max((pref_large[i - 1] if i else -1), i)
        else:
            pref_large[i] = pref_large[i - 1] if i else -1
    inf_idx = n + 5
    suf_small = [inf_idx] * (n - 1)
    for i in range(n - 2, -1, -1):
        if gap[i] < g:
            suf_small[i] = min((suf_small[i + 1] if i + 1 < n - 1 else inf_idx), i)
        else:
            suf_small[i] = suf_small[i + 1] if i + 1 < n - 1 else inf_idx

    def bad_left(k):
        return pref_bad[k - 2] if k >= 2 else 0

    def bad_right(k):
        return 0 if k >= n - 1 else tot_bad - pref_bad[k]

    def bad_bridge(k):
        if 0 < k < n - 1 and s[k + 1] - s[k - 1] < g:
            return 1
        return 0

    for k in range(n):
        bl = bad_left(k)
        br = bad_right(k)
        bb = bad_bridge(k)
        tb = bl + br + bb
        if tb > 1:
            continue
        first_t = s[0] if k != 0 else s[1]
        last_t = s[n - 1] if k != n - 1 else s[n - 2]
        if tb == 0:
            if first_t >= g + 1:
                return True
            if last_t <= m - g:
                return True
            mx = -1
            if k >= 2:
                mx = max(mx, pref_max[k - 2])
            if k + 1 <= n - 2:
                mx = max(mx, suf_max[k + 1])
            if 0 < k < n - 1:
                mx = max(mx, s[k + 1] - s[k - 1])
            if mx >= 2 * g:
                return True
            continue
        u = v = None
        if bb == 1 and bl == 0 and br == 0:
            u, v = s[k - 1], s[k + 1]
        elif bl == 1 and br == 0 and bb == 0:
            idx = pref_large[k - 2]
            u, v = s[idx], s[idx + 1]
        elif br == 1 and bl == 0 and bb == 0:
            idx = suf_small[k + 1]
            if idx > n - 2:
                continue
            u, v = s[idx], s[idx + 1]
        else:
            continue
        if v - u < 2 * g:
            continue
        L = max(1, u + g)
        R = min(m, v - g)
        if L <= R:
            return True
    return False


def solve_one(n, m, a):
    s = sorted(a)
    lo, hi = 0, m
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(n, m, s, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    t = int(input())
    outs = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        outs.append(str(solve_one(n, m, a)))
    print("\n".join(outs))


if __name__ == "__main__":
    main()
