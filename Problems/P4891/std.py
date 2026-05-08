from __future__ import annotations


def solve_interval_scheduling(n: int, intervals: list[tuple[int, int]]) -> int:
    # 按结束时间升序，相同则按开始时间升序，做经典区间调度贪心。
    intervals_sorted = sorted(intervals, key=lambda x: (x[1], x[0]))
    last_end = -(10**30)
    cnt = 0
    for s, e in intervals_sorted:
        if s > last_end:
            cnt += 1
            last_end = e
    return cnt


def main() -> None:
    n = int(input())
    parts = input().split()
    nums = list(map(int, parts))
    intervals = [(nums[2 * i], nums[2 * i + 1]) for i in range(n)]
    print(solve_interval_scheduling(n, intervals))


if __name__ == "__main__":
    main()
