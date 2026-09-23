from typing import List


class Solution:
    def longestHealthy(self, beats: List[int]) -> int:
        best = cur = 0
        for x in beats:
            if x == 1:
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 0
        return best
