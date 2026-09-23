from typing import List


class Solution:
    def minRotateCost(self, sens: List[int], baseCost: int, maxBatches: int) -> int:
        n = len(sens)
        pref = [0] * (n + 1)
        for i, x in enumerate(sens):
            pref[i + 1] = pref[i] + x
        inf = 10**30
        dp = [[inf] * (maxBatches + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(i):
                cost = baseCost + (pref[i] - pref[j]) * (i - j)
                for b in range(1, maxBatches + 1):
                    if dp[j][b - 1] + cost < dp[i][b]:
                        dp[i][b] = dp[j][b - 1] + cost
        return min(dp[n][1:])
