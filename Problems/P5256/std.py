from bisect import bisect_right


def solve(jobs):
    jobs.sort(key=lambda x: x[1])
    n = len(jobs)
    ends = [e for _s, e, _v in jobs]
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, _e, v = jobs[i - 1]
        k = bisect_right(ends, s, hi=i - 1)
        take = dp[k] + v
        skip = dp[i - 1]
        dp[i] = take if take > skip else skip
    return dp[n]


n = int(input())
jobs = []
for _ in range(n):
    s, e, v = map(int, input().split())
    jobs.append((s, e, v))
print(solve(jobs))
