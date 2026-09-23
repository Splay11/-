# -*- coding: utf-8 -*-
import math
from typing import List


class Solution:
    def predictGeneration(
        self, sub_arrays: List[List[int]], station_capacity: int
    ) -> List[int]:
        n = len(sub_arrays)
        if n == 0:
            return []

        base = [row[2] for row in sub_arrays]
        mins = [row[1] for row in sub_arrays]
        maxs = [row[0] for row in sub_arrays]

        total = sum(base)
        min_total = sum(mins)
        values = [float(x) for x in base]

        if total > station_capacity:
            need = total - station_capacity
            spaces = [base[i] - mins[i] for i in range(n)]
            space_sum = sum(spaces)
            if space_sum == 0:
                return [0] * n
            for i in range(n):
                values[i] = base[i] - need * spaces[i] / space_sum
        elif total < min_total:
            need = min_total - total
            spaces = [maxs[i] - base[i] for i in range(n)]
            space_sum = sum(spaces)
            if space_sum == 0:
                return [0] * n
            for i in range(n):
                values[i] = base[i] + need * spaces[i] / space_sum

        return [math.ceil(v - 1e-12) for v in values]
