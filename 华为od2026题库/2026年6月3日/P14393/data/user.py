from typing import List
from collections import deque

class Solution:
    def canIsolateWithTwoPools(
        self, resourceCount: List[int], conflicts: List[List[List[int]]]
    ) -> List[int]:
        return [0] * len(resourceCount)
