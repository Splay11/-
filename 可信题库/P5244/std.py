# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def minComputeCost(
        self, load: List[int], runCost: int, changeCost: int, maxChanges: int
    ) -> int:
        n = len(load)
        M = max(load) if load else 0
        INF = 10**18
        # prev[c][p]：已用 c 次变更、当前实例数为 p 的最小费用
        prev = [{} for _ in range(maxChanges + 1)]
        prev[0][0] = 0
        for i in range(n):
            cur = [{} for _ in range(maxChanges + 1)]
            for c in range(maxChanges + 1):
                for p, cost in prev[c].items():
                    for x in range(load[i], M + 1):
                        nc = c + (0 if x == p else 1)
                        if nc > maxChanges:
                            continue
                        nc_cost = cost + x * runCost + abs(x - p) * changeCost
                        if x not in cur[nc] or nc_cost < cur[nc][x]:
                            cur[nc][x] = nc_cost
            prev = cur
        ans = INF
        for c in range(maxChanges + 1):
            if prev[c]:
                ans = min(ans, min(prev[c].values()))
        return ans
