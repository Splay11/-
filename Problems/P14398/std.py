# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def sortConvertedNums(self, nums: List[int], base: int) -> List[str]:
        def to_base(n: int) -> str:
            if n == 0:
                return "0"
            digits = "0123456789abcdef"
            parts = []
            while n:
                parts.append(digits[n % base])
                n //= base
            return "".join(reversed(parts))

        pairs = [(x, to_base(x)) for x in nums]
        pairs.sort(key=lambda p: p[0], reverse=True)
        return [s for _, s in pairs]
