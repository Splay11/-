# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def findMaintenanceWindow(self, n: int, w: int, scores: List[int]) -> List[int]:
        if n < w:
            return [-1, 0]

        window_sum = 0
        zero_count = 0
        for i in range(w):
            window_sum += scores[i]
            if scores[i] == 0:
                zero_count += 1

        best_start = -1
        min_sum = 10**18
        if zero_count == 0:
            min_sum = window_sum
            best_start = 0

        for start in range(1, n - w + 1):
            out_val = scores[start - 1]
            in_val = scores[start + w - 1]
            window_sum += in_val - out_val
            if out_val == 0:
                zero_count -= 1
            if in_val == 0:
                zero_count += 1
            if zero_count == 0 and window_sum < min_sum:
                min_sum = window_sum
                best_start = start

        if best_start == -1:
            return [-1, 0]
        return [best_start, min_sum]
