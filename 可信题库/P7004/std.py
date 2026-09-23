from typing import List


class Solution:
    def minArchiveCap(self, logs: List[int], limitDays: int) -> int:
        def need(cap: int) -> int:
            # 贪心：同一天尽量连续装完整包，和不超过 cap
            days = 1
            cur = 0
            for x in logs:
                if cur + x > cap:
                    days += 1
                    cur = 0
                cur += x
            return days

        lo, hi = max(logs), sum(logs)
        while lo < hi:
            mid = (lo + hi) // 2
            if need(mid) <= limitDays:
                hi = mid
            else:
                lo = mid + 1
        return lo
