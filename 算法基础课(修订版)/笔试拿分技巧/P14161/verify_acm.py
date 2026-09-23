from collections import defaultdict


class Solution:
    def solve(self, times, mutex_pairs):
        job_num = len(times)
        mutex = defaultdict(set)
        for a, b in mutex_pairs:
            u, v = a - 1, b - 1
            mutex[u].add(v)
            mutex[v].add(u)

        ans = 1
        cost = float("inf")

        def check(i, usd):
            for u in usd:
                if i in mutex[u] or u in mutex[i]:
                    return False
            return True

        def dfs(i, usd, time):
            nonlocal ans, cost
            if i >= job_num:
                if ans <= len(usd):
                    if ans < len(usd):
                        ans = len(usd)
                        cost = time
                    elif time < cost:
                        cost = time
                return
            if len(usd) + job_num - i + 1 < ans:
                return
            dfs(i + 1, usd, time)
            if check(i, usd):
                usd.add(i)
                dfs(i + 1, usd, time + times[i])
                usd.remove(i)

        dfs(0, set(), 0)
        return int(cost)


if __name__ == "__main__":
    job_num = int(input())
    times = list(map(int, input().split()))
    mutex_num = int(input())
    mutex_pairs = [tuple(map(int, input().split())) for _ in range(mutex_num)]

    solution = Solution()
    print(solution.solve(times, mutex_pairs))
