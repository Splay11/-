def solve(intervals):
    """按右端点从小到大排序，贪心保留能放下的区间。
    只在端点相碰不算重叠，所以下一个区间的左端点只要 >= 已保留的右端点就可以留下。
    最少删除数 = 总数 - 最多保留数。
    """
    intervals.sort(key=lambda x: x[1])
    keep = 0
    last_end = -10**9
    for start, end in intervals:
        if start >= last_end:
            # 与已保留区间不重叠（含端点相碰），可以留下
            keep += 1
            last_end = end
    return len(intervals) - keep


def main():
    # 第一行 n，接下来 n 行每个区间的左右端点
    n = int(input())
    intervals = []
    for _ in range(n):
        s, e = map(int, input().split())
        intervals.append((s, e))
    print(solve(intervals))


if __name__ == "__main__":
    main()
