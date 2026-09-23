from typing import List


class Solution:
    def maxMaintenanceScore(self, windows: List[List[int]]) -> int:
        # 过滤非法区间，按结束时间排序
        a = [x for x in windows if x[1] > x[0]]
        if not a:
            return 0
        a.sort(key=lambda x: x[1])
        n = len(a)
        ends = [x[1] for x in a]
        dp = [0] * (n + 1)  # dp[i]：考虑前 i 个窗口

        for i in range(1, n + 1):
            s, e, sc = a[i - 1]
            # 二分找最右的 j，使 ends[j] <= s（与当前不相交）
            lo, hi, p = 0, i - 2, -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if ends[mid] <= s:
                    p = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            take = sc + (dp[p + 1] if p >= 0 else 0)
            # 负分自然会被「不选」盖掉
            dp[i] = max(dp[i - 1], take)
        return dp[n]
