# -*- coding: utf-8 -*-
from collections import deque
from typing import List


class Solution:
    def canIsolateWithTwoPools(
        self, resourceCount: List[int], conflicts: List[List[List[int]]]
    ) -> List[int]:
        ans = []
        # 每组独立建图，判断是否为二分图
        for n, edges in zip(resourceCount, conflicts):
            ans.append(1 if self._bipartite(n, edges) else 0)
        return ans

    def _bipartite(self, n: int, edges: List[List[int]]) -> bool:
        # 自环：同一资源与自己互斥，两池无法划分
        for u, v in edges:
            if u == v:
                return False

        # 无向图邻接表，顶点编号 1..n
        adj = [[] for _ in range(n + 1)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        color = [-1] * (n + 1)  # -1 表示未染色
        for start in range(1, n + 1):
            # 已染色或无边的孤立点跳过
            if color[start] != -1 or not adj[start]:
                continue
            color[start] = 0
            q = deque([start])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        # 互斥边两端必须异色，对应两个资源池
                        color[v] = 1 - color[u]
                        q.append(v)
                    elif color[v] == color[u]:
                        # 相邻同色 → 奇环，不是二分图
                        return False
        return True
