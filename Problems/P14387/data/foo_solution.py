# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def maxChargingDemand(self, n: int, m: int, k: int, demands: List[int]) -> int:
        neg = -(10**18)
        dp = [[neg] * (m + 1) for _ in range(n)]
        best = [neg] * (m + 1)
        ans = 0

        for i in range(n):
            if i >= k:
                for c in range(1, m + 1):
                    best[c] = max(best[c], dp[i - k][c])
            dp[i][1] = demands[i]
            for c in range(2, m + 1):
                if best[c - 1] != neg:
                    dp[i][c] = best[c - 1] + demands[i]
            ans = max(ans, dp[i][m])

        return ans
