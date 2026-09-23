from typing import List
import heapq


class Solution:
    def minTrustDelay(
        self, n: int, edges: List[List[int]], src: int, dst: int, riskBudget: int
    ) -> int:
        if src == dst:
            return 0
        g = [[] for _ in range(n)]
        for u, v, d, r in edges:
            g[u].append((v, d, r))
        inf = 10**18
        dist = [[inf] * (riskBudget + 1) for _ in range(n)]
        dist[src][0] = 0
        pq = [(0, src, 0)]
        while pq:
            delay, u, used = heapq.heappop(pq)
            if delay != dist[u][used]:
                continue
            if u == dst:
                return delay
            for v, w, r in g[u]:
                nu = used + r
                if nu > riskBudget:
                    continue
                nd = delay + w
                if nd < dist[v][nu]:
                    dist[v][nu] = nd
                    heapq.heappush(pq, (nd, v, nu))
        return -1
