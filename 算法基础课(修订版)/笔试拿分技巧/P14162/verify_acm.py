import heapq


class Solution:
    def solve(self, n, k, intervals):
        intervals.sort(key=lambda x: x[0])
        start = 0
        heap = []
        idx = 0
        ans = 0

        while idx < n or heap:
            while heap and heap[0] < start:
                heapq.heappop(heap)

            while idx < n and intervals[idx][0] <= start:
                heapq.heappush(heap, intervals[idx][1])
                idx += 1

            if not heap:
                if idx == n:
                    break
                start = max(start, intervals[idx][0])

            while idx < n and intervals[idx][0] <= start:
                heapq.heappush(heap, intervals[idx][1])
                idx += 1

            for _ in range(k):
                if heap:
                    ans += 1
                    heapq.heappop(heap)

            start += 1

        return ans


if __name__ == "__main__":
    n, k = map(int, input().split())
    intervals = [list(map(int, input().split())) for _ in range(n)]

    solution = Solution()
    print(solution.solve(n, k, intervals))
