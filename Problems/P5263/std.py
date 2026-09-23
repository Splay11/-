def min_bottleneck(layers, m):
    def can(limit):
        cnt = 1
        s = 0
        for x in layers:
            if s + x > limit:
                cnt += 1
                s = 0
            s += x
        return cnt <= m

    lo, hi = max(layers), sum(layers)
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":
    n = int(input())
    layers = list(map(int, input().split()))
    m = int(input())
    print(min_bottleneck(layers, m))
