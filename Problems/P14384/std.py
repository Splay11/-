# -*- coding: utf-8 -*-
import heapq
from typing import List


class Solution:
    def countFailedCharging(self, n: int, cars: List[List[int]]) -> int:
        events = []
        for i, (at, _ct, _wt) in enumerate(cars):
            heapq.heappush(events, (at, 1, "A", i))

        piles = [0] * n
        heapq.heapify(piles)
        waiting = []
        failed = 0

        while events:
            t = events[0][0]
            batch = []
            while events and events[0][0] == t:
                batch.append(heapq.heappop(events))
            batch.sort(key=lambda x: x[1])

            for _time, _pri, kind, data in batch:
                if kind == "F":
                    heapq.heappush(piles, t)
                else:
                    waiting.append(data)

            while piles and piles[0] <= t and waiting:
                car = waiting[0]
                at, ct, wt = cars[car]
                if t - at > wt:
                    waiting.pop(0)
                    failed += 1
                    continue
                heapq.heappop(piles)
                finish = t + ct
                heapq.heappush(events, (finish, 0, "F", 0))
                waiting.pop(0)

        return failed
