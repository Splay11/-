# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List


class Solution:
    def maxZoneImbalance(self, loads: List[int], edges: List[List[int]]) -> int:
        n = len(loads)
        if not edges:
            return -1
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for u, v in edges:
            union(u, v)

        groups: defaultdict[int, list] = defaultdict(list)
        for i in range(n):
            groups[find(i)].append(i)

        ans = -1
        for nodes in groups.values():
            if len(nodes) < 2:
                continue
            vals = [loads[i] for i in nodes]
            imbalance = (max(vals) - min(vals)) * len(nodes)
            ans = max(ans, imbalance)
        return ans
