# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def minimumLatency(self, nums: List[int], k: int) -> int:
        def can(limit: int) -> bool:
            cnt = 1
            s = 0
            for x in nums:
                if s + x > limit:
                    cnt += 1
                    s = 0
                s += x
            return cnt <= k

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
