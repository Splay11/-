# -*- coding: utf-8 -*-
from typing import List
from collections import defaultdict, deque


class Solution:
    def minRebuildTime(
        self, n: int, deps: List[List[int]], buildTime: List[int], changed: List[int]
    ) -> int:
        dependents = defaultdict(list)  # b -> a：谁依赖 b
        depends_on = defaultdict(list)  # a -> b：a 依赖谁
        for a, b in deps:
            dependents[b].append(a)
            depends_on[a].append(b)

        # 从 changed 沿反向依赖扩散，得到重建集合
        need = set()
        q = deque()
        for x in changed:
            if x not in need:
                need.add(x)
                q.append(x)
        while q:
            u = q.popleft()
            for v in dependents[u]:
                if v not in need:
                    need.add(v)
                    q.append(v)

        if not need:
            return 0

        # 仅在重建集合内拓扑：入度为「仍在集合内的依赖」个数
        indeg = {u: 0 for u in need}
        for u in need:
            for b in depends_on[u]:
                if b in need:
                    indeg[u] += 1

        qq = deque([u for u in need if indeg[u] == 0])
        finish = {}
        while qq:
            u = qq.popleft()
            mx = 0
            for b in depends_on[u]:
                if b in need:
                    mx = max(mx, finish[b])
            finish[u] = mx + buildTime[u]
            for v in dependents[u]:
                if v in need:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        qq.append(v)

        return max(finish.values())
