# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def maxSolarPanelArea(self, heights: List[int]) -> int:
        left, right = 0, len(heights) - 1
        best = 0
        while left < right:
            h = heights[left] if heights[left] < heights[right] else heights[right]
            area = h * (right - left)
            if area > best:
                best = area
            if heights[left] <= heights[right]:
                left += 1
            else:
                right -= 1
        return best
