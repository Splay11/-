# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def packFields(self, sectionWidth: List[int], sectionValues: List[int]) -> str:
        acc = 0
        total = 0
        for w, v in zip(sectionWidth, sectionValues):
            acc = (acc << w) | v
            total += w
        pad = (8 - total % 8) % 8
        acc <<= pad
        total += pad
        nbytes = total // 8
        return f"{acc:0{nbytes * 2}X}"
