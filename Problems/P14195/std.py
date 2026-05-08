# -*- coding: utf-8 -*-
from collections import defaultdict, deque
from typing import Dict, List


class Solution:
    def allBuildOrders(self, modules: List[str], dependencies: List[List[str]]) -> List[str]:
        if not modules:
            return []
        indeg: Dict[str, int] = {m: 0 for m in modules}
        g: Dict[str, List[str]] = defaultdict(list)
        for edge in dependencies:
            a, b = edge[0], edge[1]
            if a not in indeg or b not in indeg:
                continue
            g[b].append(a)
            indeg[a] += 1

        q = deque([m for m in modules if indeg[m] == 0])
        tmp = indeg.copy()
        seen = 0
        while q:
            u = q.popleft()
            seen += 1
            for v in g[u]:
                tmp[v] -= 1
                if tmp[v] == 0:
                    q.append(v)
        if seen != len(modules):
            return []

        indeg_mut = indeg.copy()
        path: List[str] = []
        out: List[str] = []

        def dfs() -> None:
            if len(path) == len(modules):
                out.append(" ".join(path))
                return
            cand = sorted([m for m in modules if m not in path and indeg_mut[m] == 0])
            for m in cand:
                path.append(m)
                for nei in g[m]:
                    indeg_mut[nei] -= 1
                dfs()
                for nei in g[m]:
                    indeg_mut[nei] += 1
                path.pop()

        dfs()
        return sorted(out)
