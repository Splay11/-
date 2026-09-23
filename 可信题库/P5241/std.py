import heapq
from typing import List


class Solution:
    def finishTimes(
        self, arrival: List[int], duration: List[int], priority: List[int]
    ) -> List[int]:
        n = len(arrival)
        rem = duration[:]
        ans = [-1] * n
        order = sorted(range(n), key=lambda i: (arrival[i], i))
        ready: List[tuple] = []  # (-priority, index)
        time = 0
        i = 0
        cur = None

        while i < n or ready or cur is not None:
            if cur is None and not ready:
                if i >= n:
                    break
                time = max(time, arrival[order[i]])

            while i < n and arrival[order[i]] <= time:
                idx = order[i]
                heapq.heappush(ready, (-priority[idx], idx))
                i += 1

            if cur is not None:
                if ready and (ready[0][0], ready[0][1]) < (-priority[cur], cur):
                    heapq.heappush(ready, (-priority[cur], cur))
                    cur = heapq.heappop(ready)[1]
            else:
                if not ready:
                    continue
                cur = heapq.heappop(ready)[1]

            next_arr = arrival[order[i]] if i < n else None
            finish = time + rem[cur]
            if next_arr is not None and next_arr < finish:
                rem[cur] -= next_arr - time
                time = next_arr
            else:
                time = finish
                ans[cur] = time
                rem[cur] = 0
                cur = None

        return ans
