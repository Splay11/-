from collections import deque
import sys


def has_cycle(n: int, edges) -> bool:
    """拓扑排序判有向环：若无法排出全部点则有环。"""
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    cnt = 0
    while q:
        u = q.popleft()
        cnt += 1
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return cnt != n


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        edges.append((u, v))
    print("YES" if has_cycle(n, edges) else "NO")


if __name__ == "__main__":
    main()
