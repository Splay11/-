# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def countIsolatedIntervals(self, intervals: List[List[int]]) -> int:
        n = len(intervals)
        ans = 0
        for i in range(n):
            s1, e1 = intervals[i]
            isolated = True
            for j in range(n):
                if i == j:
                    continue
                s2, e2 = intervals[j]
                if s1 <= e2 and s2 <= e1:
                    isolated = False
                    break
            if isolated:
                ans += 1
        return ans
