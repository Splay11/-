from typing import List

class Solution:
    def countMinefields(self, isChainExplosion: List[List[int]]) -> int:
        n = len(isChainExplosion)
        visited = [False] * n
        count = 0

        def dfs(u: int) -> None:
            """深度优先搜索标记同一雷区的所有地震雷"""
            visited[u] = True
            for v in range(n):
                if isChainExplosion[u][v] == 1 and not visited[v]:
                    dfs(v)

        for i in range(n):
            if not visited[i]:
                # 发现一个新的雷区
                count += 1
                dfs(i)
        return count
