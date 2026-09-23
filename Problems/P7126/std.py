def can_attend_all(intervals):
    """按开始时间排序后，检查是否有一场在上一场结束前就开始。结束时刻等于下一场开始不算冲突。"""
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        # 当前场开始时间若早于上一场结束时间，两场有重叠
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


def main():
    # 第一行：面试场数
    n = int(input())
    intervals = []
    for _ in range(n):
        s, e = map(int, input().split())
        intervals.append((s, e))
    # 能全部参加输出 YES，否则 NO
    print("YES" if can_attend_all(intervals) else "NO")


if __name__ == "__main__":
    main()
