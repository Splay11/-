# -*- coding: utf-8 -*-
from collections import Counter
from typing import List


class Solution:
    def countProfilePairs(self, profiles: List[int], diff: int) -> int:
        if diff == 0:
            cnt = Counter(profiles)
            return sum(1 for c in cnt.values() if c >= 2)
        seen = set(profiles)
        return sum(1 for v in seen if (v + diff) in seen)
