from collections import Counter


def can_finish(c, q, w, h, freq, days):
    # 判定：在 days 天内能不能打掉 q 块矿岩
    if days <= 0:
        return False
    # days = full 个完整周期 + 多出来的 rest 天
    full, rest = divmod(days, c)
    done = 0
    for x, cnt in freq:
        if x <= w:
            # 初始功率已经够打这个硬度，每个完整周期都能打一次
            add = full
        else:
            # 完整周期里功率依次是 w, w+1, ..., w+full-1
            # 要功率 >= x，需要过完 x-w 个周期之后才开始贡献
            add = full - (x - w)
            if add < 0:
                add = 0
        if add == 0:
            continue
        done += add * cnt
        if done >= q:
            return True
    # 多出来的 rest 天功率固定为 w+full，对应周期前 rest 个位置
    atk = w + full
    for i in range(rest):
        if h[i] <= atk:
            done += 1
            if done >= q:
                return True
    return done >= q


def min_days(c, q, w, h):
    # 相同硬度合并计数，避免二分时反复扫同一批值
    freq = list(Counter(h).items())
    # 天数越多越容易打完，对天数二分找最小可行值
    lo = 1
    hi = 4 * 10**18
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_finish(c, q, w, h, freq, mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans


def main():
    c, q, w = map(int, input().split())
    h = list(map(int, input().split()))
    print(min_days(c, q, w, h))


if __name__ == "__main__":
    main()
