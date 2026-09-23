# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import List


class Solution:
    def countHikingPaths(self, grid: List[List[int]], maxDiff: int) -> int:
        n = len(grid)
        m = len(grid[0])
        flat = [grid[i][j] for i in range(n) for j in range(m)]
        mn, mx = min(flat), max(flat)
        si = sj = ei = ej = -1
        for i in range(n):
            for j in range(m):
                if grid[i][j] == mn:
                    si, sj = i, j
                if grid[i][j] == mx:
                    ei, ej = i, j
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

        @lru_cache(maxsize=None)
        def dfs(i: int, j: int) -> int:
            if i == ei and j == ej:
                return 1
            h = grid[i][j]
            tot = 0
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m:
                    nh = grid[ni][nj]
                    d = nh - h
                    if d > 0 and d <= maxDiff:
                        tot += dfs(ni, nj)
            return tot

        return dfs(si, sj)
