# -*- coding: utf-8 -*-
from collections import deque
from typing import List


class Solution:
    def countShortestPaths(self, n: int, guards: List[List[int]]) -> List[int]:
        sx, sy = 0, n // 2
        ex, ey = n - 1, n // 2
        ban = [[False] * n for _ in range(n)]
        for g in guards:
            gx, gy = int(g[0]), int(g[1])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = gx + dx, gy + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        ban[nx][ny] = True
        if ban[sx][sy] or ban[ex][ey]:
            return [0, 0]
        dist = [[-1] * n for _ in range(n)]
        ways = [[0] * n for _ in range(n)]
        dist[sx][sy] = 0
        ways[sx][sy] = 1
        q = deque([(sx, sy)])
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
        while q:
            x, y = q.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= n or ny < 0 or ny >= n or ban[nx][ny]:
                    continue
                if dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    ways[nx][ny] = ways[x][y]
                    q.append((nx, ny))
                elif dist[nx][ny] == dist[x][y] + 1:
                    ways[nx][ny] += ways[x][y]
        if dist[ex][ey] == -1:
            return [0, 0]
        return [ways[ex][ey], dist[ex][ey] + 1]
