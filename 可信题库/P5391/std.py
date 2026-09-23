from typing import List


class Solution:
    def canPassBooks(self, desks: List[int]) -> bool:
        s = 0
        for i, x in enumerate(desks):
            s += x
            k = i + 1
            if s < k * (k + 1) // 2:
                return False
        return True
