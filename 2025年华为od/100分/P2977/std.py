# -*- coding: utf-8 -*-
from collections import deque
from typing import List


class Solution:
    def simulateTaskQueue(
        self,
        submitTimes: List[int],
        execTimes: List[int],
        queueCapacity: int,
        numWorkers: int,
    ) -> List[int]:
        queue = deque()
        discarded = 0
        last_finish = 0
        m = numWorkers

        # free_at[i] == 0 表示执行者 i 当前空闲；否则为最早可接新任务的时刻
        free_at = [0] * (m + 1)

        subs = sorted(zip(submitTimes, execTimes))
        si = 0
        n = len(subs)

        def assign(time: int) -> None:
            nonlocal last_finish
            idle = sorted(i for i in range(1, m + 1) if free_at[i] <= time)
            for wid in idle:
                if not queue:
                    break
                dur = queue.popleft()
                finish = time + dur
                last_finish = max(last_finish, finish)
                free_at[wid] = finish

        while True:
            busy = [free_at[i] for i in range(1, m + 1) if free_at[i] > 0]
            if si >= n and not queue and not busy:
                break

            next_submit = subs[si][0] if si < n else 10**18
            next_free = min(busy) if busy else 10**18
            t = min(next_submit, next_free)

            for i in range(1, m + 1):
                if free_at[i] > 0 and free_at[i] <= t:
                    free_at[i] = 0

            assign(t)

            while si < n and subs[si][0] == t:
                d = subs[si][1]
                if len(queue) >= queueCapacity:
                    queue.popleft()
                    discarded += 1
                queue.append(d)
                si += 1

            assign(t)

        return [last_finish, discarded]
