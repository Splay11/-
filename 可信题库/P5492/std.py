from typing import List


class Solution:
    def maxLoadDrop(self, loads: List[int]) -> int:
        peak = loads[0]
        ans = 0
        for x in loads:
            if peak - x > ans:
                ans = peak - x
            if x > peak:
                peak = x
        return ans
