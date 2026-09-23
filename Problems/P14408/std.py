# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def selectMaxWeightPolicies(
        self, n: int, k: int, weights: List[int], conflicts: List[List[int]]
    ) -> List[List[int]]:
        if k < 0 or k > n:
            return []

        conflict_mask = [0] * n
        for a, b in conflicts:
            conflict_mask[a - 1] |= 1 << (b - 1)
            conflict_mask[b - 1] |= 1 << (a - 1)

        def is_independent(mask: int) -> bool:
            m = mask
            while m:
                lsb = m & -m
                i = lsb.bit_length() - 1
                if conflict_mask[i] & mask:
                    return False
                m ^= lsb
            return True

        best = None
        result: List[List[int]] = []
        for mask in range(1 << n):
            if bin(mask).count("1") != k:
                continue
            if not is_independent(mask):
                continue
            total = sum(weights[i] for i in range(n) if mask & (1 << i))
            combo = [i + 1 for i in range(n) if mask & (1 << i)]
            if best is None or total > best:
                best = total
                result = [combo]
            elif total == best:
                result.append(combo)

        if best is None:
            return []
        return result
