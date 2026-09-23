# 有序数组上用二分求 T 的首次/末次出现，以及严格小于/大于 T 的边界下标


def query_positions(a, T):
    n = len(a)

    # 求第一个 >= T 的下标（即 lower_bound），找不到则等于 n
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if a[mid] < T:
            left = mid + 1
        else:
            right = mid
    lower = left

    # 求第一个 > T 的下标（即 upper_bound），找不到则等于 n
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if a[mid] <= T:
            left = mid + 1
        else:
            right = mid
    upper = left

    # T 的首次出现就是 lower；该位置越界或值不是 T 则不存在
    first = lower if lower < n and a[lower] == T else -1
    # T 的末次出现就是 upper-1；该位置合法且值是 T 才算找到
    last = upper - 1 if upper > 0 and a[upper - 1] == T else -1
    # 小于 T 的数全在 lower 左侧，最大下标是 lower-1
    pred = lower - 1 if lower > 0 else -1
    # 大于 T 的数从 upper 开始，越界则不存在
    succ = upper if upper < n else -1
    return first, last, pred, succ


def main():
    # 第一行：长度与目标值
    n, T = map(int, input().split())
    # 第二行：非递减数组
    a = list(map(int, input().split()))
    first, last, pred, succ = query_positions(a, T)
    print(first, last, pred, succ)


if __name__ == "__main__":
    main()
