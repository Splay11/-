# -*- coding: utf-8 -*-
from typing import List


def popcount32(x: int) -> int:
    return bin(x & 0xFFFFFFFF).count("1")


class Solution:
    def processDataArray(self, data: List[int], operations: List[List[int]]) -> List[int]:
        arr = list(data)

        def sort_arr() -> None:
            arr.sort(key=lambda v: (popcount32(v), v))

        sort_arr()
        for op in operations:
            i, j = op[0], op[1]
            a = arr[i]
            b = arr[j] if i != j else a
            merged = a | b
            if i == j:
                arr.pop(i)
            else:
                lo, hi = min(i, j), max(i, j)
                arr.pop(hi)
                arr.pop(lo)
            arr.append(merged)
            sort_arr()
        return arr
