# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def analyzeTemperatureData(
        self, temperatures: List[int], k: int, t: int
    ) -> List[int]:
        n = len(temperatures)
        max_val = temperatures[0]
        max_idx = 0
        for i in range(1, n):
            if temperatures[i] > max_val:
                max_val = temperatures[i]
                max_idx = i

        count = 0
        best_start = -1
        best_end = -1
        best_rise = -1

        for i in range(0, n - k + 1):
            ok = True
            for j in range(i, i + k - 1):
                if temperatures[j] >= temperatures[j + 1]:
                    ok = False
                    break
            if not ok:
                continue
            rise = temperatures[i + k - 1] - temperatures[i]
            if rise >= t:
                count += 1
                if rise > best_rise or (
                    rise == best_rise and (best_start == -1 or i < best_start)
                ):
                    best_rise = rise
                    best_start = i
                    best_end = i + k - 1

        return [max_val, max_idx, count, best_start, best_end]
