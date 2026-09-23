from typing import List


class Solution:
    def maxImpactReach(self, n: int, links: List[List[int]], level: List[int]) -> int:
        if n <= 0:
            return 0
        # 先建成无向图，再从 0 定根得到孩子列表
        g = [[] for _ in range(n)]
        for u, v in links:
            g[u].append(v)
            g[v].append(u)
        children = [[] for _ in range(n)]
        parent = [-1] * n
        q = [0]
        parent[0] = -2
        for u in q:
            for v in g[u]:
                if parent[v] == -1:
                    parent[v] = u
                    children[u].append(v)
                    q.append(v)

        # 状态 (节点, 是否已用特批)；显式栈 DFS
        vis = [[False, False] for _ in range(n)]
        seen = [False] * n
        st = [(0, 0)]
        vis[0][0] = True
        while st:
            u, used = st.pop()
            seen[u] = True
            for v in children[u]:
                if level[u] > level[v]:
                    nu = used  # 正常通行
                elif used == 0:
                    nu = 1     # 消耗特批
                else:
                    continue
                if not vis[v][nu]:
                    vis[v][nu] = True
                    st.append((v, nu))
        return sum(1 for x in seen if x)
