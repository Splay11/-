# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def minimizeRangeSum(self, n: int, nums: List[int]) -> int:
        a = sorted(nums)
        if n == 2:
            return 0
        ans = a[-1] - a[0]
        for i in range(n - 1):
            cost = (a[i] - a[0]) + (a[-1] - a[i + 1])
            if cost < ans:
                ans = cost
        return ans
