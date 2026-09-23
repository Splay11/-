from typing import List


class Solution:
    def minPassDays(self, slots: List[int], prep: List[int]) -> int:
        n, m = len(slots), len(prep)

        def ok(days: int) -> bool:
            # 前 days 天内，每门课取最后一次可考日；按考试日从早到晚贪心扣复习额度
            last = [-1] * (m + 1)
            for i in range(days):
                t = slots[i]
                if t > 0:
                    last[t] = i
            for t in range(1, m + 1):
                if last[t] < 0:
                    return False
            order = sorted(range(1, m + 1), key=lambda t: last[t])
            free = 0
            j = 0
            for day in range(days):
                if j < m and last[order[j]] == day:
                    need = prep[order[j] - 1]
                    if free < need:
                        return False
                    free -= need
                    j += 1
                else:
                    free += 1
            return j == m

        if not ok(n):
            return -1
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
