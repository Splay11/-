from typing import List
import bisect


class Solution:
    def countLiveWindows(self, loads: List[int], cap: int) -> int:
        n = len(loads)
        pref = [0] * (n + 1)
        for i, x in enumerate(loads):
            pref[i + 1] = pref[i] + x
        # dp[i]：以 i 为左端点的存活窗口个数（后缀 DP）
        dp = [0] * (n + 2)
        for i in range(n - 1, -1, -1):
            # 找最小 q，使 pref[q] > pref[i] + cap，即 (i..q-1] 首次超阈
            q = bisect.bisect_right(pref, pref[i] + cap)
            dp[i] = dp[q] + (q - i - 1)
        return sum(dp[: n + 1])
