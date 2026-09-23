from collections import defaultdict, deque
from typing import List


class Solution:
    def countKeptAlarms(self, events: List[List[int]], window: int, limit: int) -> int:
        # 每种类型独立维护已保留告警时间戳队列
        dq = defaultdict(deque)
        kept = 0
        for t, typ in events:
            q = dq[typ]
            # 弹出不在 (t-window, t] 内的历史；window=0 时保留同刻已保留项
            while q and q[0] <= t - window and q[0] < t:
                q.popleft()
            if len(q) < limit:
                q.append(t)
                kept += 1
        return kept
