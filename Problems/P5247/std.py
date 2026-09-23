import bisect


def enum_sums(arr):
    n = len(arr)
    by_cnt = [[] for _ in range(n + 1)]
    for mask in range(1 << n):
        s = 0
        c = 0
        for i in range(n):
            if mask >> i & 1:
                s += arr[i]
                c += 1
        by_cnt[c].append(s)
    for c in range(n + 1):
        by_cnt[c].sort()
    return by_cnt


def min_diff(vals):
    n = len(vals)
    half = n // 2
    tot = sum(vals)
    left = vals[:half]
    right = vals[half:]
    sl = enum_sums(left)
    sr = enum_sums(right)
    best = tot
    for k in range(half + 1):
        A = sl[k]
        B = sr[half - k]
        if not A or not B:
            continue
        for x in A:
            t = tot // 2 - x
            i = bisect.bisect_left(B, t)
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(B):
                    s = x + B[j]
                    d = tot - 2 * s
                    if d < 0:
                        d = -d
                    if d < best:
                        best = d
    return best


def main():
    q = int(input())
    for _ in range(q):
        int(input())
        vals = list(map(int, input().split()))
        print(min_diff(vals))


if __name__ == "__main__":
    main()
