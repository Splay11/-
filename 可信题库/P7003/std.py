from collections import deque
from typing import List


class Solution:
    def minFinishTime(self, n: int, prev: List[int], next: List[int], time: List[int]) -> int:
        g = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v in zip(prev, next):
            g[u].append(v)
            indeg[v] += 1
        finish = [0] * n
        q = deque()
        for i in range(n):
            if indeg[i] == 0:
                finish[i] = time[i]
                q.append(i)
        seen = 0
        while q:
            u = q.popleft()
            seen += 1
            for v in g[u]:
                # 完工时间 = 前置最大完工 + 自身耗时
                if finish[u] + time[v] > finish[v]:
                    finish[v] = finish[u] + time[v]
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        if seen != n:
            return -1
        return max(finish) if n else -1
