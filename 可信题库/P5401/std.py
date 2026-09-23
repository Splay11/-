from typing import List


class Solution:
    def minForceWindow(self, hits: List[int]) -> int:
        n = len(hits)
        tot = 0
        for x in hits:
            tot |= x
        if tot == 0:
            return 1
        ans = 1
        for b in range(31):
            if ((tot >> b) & 1) == 0:
                continue
            prev = -1
            mx = 0
            for i, x in enumerate(hits):
                if (x >> b) & 1:
                    mx = max(mx, i - prev)
                    prev = i
            mx = max(mx, n - prev)
            ans = max(ans, mx)
        return ans
