V = 1000


def min_side(k, cols, rows):
    # 只要求框到 1 件时，任意一格的边长都是 1
    if k <= 1:
        return 1
    width = V + 1
    # 列、行都从 1 编号，把每件货记到对应方格
    grid = [0] * (width * width)
    for c, r in zip(cols, rows):
        grid[c * width + r] = 1
    # ps[c][r] 表示列 1..c、行 1..r 这一块里的件数
    ps = [0] * (width * width)
    for c in range(1, V + 1):
        running = 0
        cur = c * width
        prev = (c - 1) * width
        for r in range(1, V + 1):
            running += grid[cur + r]
            ps[cur + r] = ps[prev + r] + running

    def enough(side):
        # 枚举左上角，统计边长为 side 的闭区间里有多少件货
        span = side - 1
        last = V - span
        for c in range(1, last + 1):
            hi = (c + span) * width
            lo = (c - 1) * width
            for r in range(1, last + 1):
                r2 = r + span
                total = ps[hi + r2] - ps[hi + r - 1] - ps[lo + r2] + ps[lo + r - 1]
                if total >= k:
                    return True
        return False

    # 边长越大越容易凑够 k 件，二分最小可行边长
    low, high = 1, V
    while low < high:
        mid = (low + high) // 2
        if enough(mid):
            high = mid
        else:
            low = mid + 1
    return low


def main():
    k = int(input())
    p = int(input())
    cols = list(map(int, input().split()))
    rows = list(map(int, input().split()))
    print(min_side(k, cols, rows))


if __name__ == "__main__":
    main()
