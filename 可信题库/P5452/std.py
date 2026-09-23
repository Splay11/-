# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def minCircleMerge(self, weights: List[int]) -> int:
        n = len(weights)
        if n <= 1:
            return 0
        if n == 2:
            return weights[0] + weights[1]

        m = 2 * n
        a = weights + weights
        pref = [0] * (m + 1)
        for i in range(m):
            pref[i + 1] = pref[i] + a[i]

        INF = 10**18
        dp = [[0] * m for _ in range(m)]
        opt = [[0] * m for _ in range(m)]
        for i in range(m):
            opt[i][i] = i

        for length in range(2, n + 1):
            for i in range(0, m - length + 1):
                j = i + length - 1
                lo = opt[i][j - 1]
                hi = opt[i + 1][j] if i + 1 <= j else j - 1
                if hi > j - 1:
                    hi = j - 1
                best = INF
                bk = lo
                for k in range(lo, hi + 1):
                    cur = dp[i][k] + dp[k + 1][j]
                    if cur < best:
                        best = cur
                        bk = k
                dp[i][j] = best + (pref[j + 1] - pref[i])
                opt[i][j] = bk

        ans = INF
        for i in range(n):
            ans = min(ans, dp[i][i + n - 1])
        return int(ans)
