# 按质量排序后，把热度能互相罩住的稿件并到同一连通块；块内可任意重排

from heapq import heappush, heappop
from collections import defaultdict


def can_match(p, h, t):
    """
    两条稿可对调当且仅当质量、热度都满足分量偏序。
    可比关系的连通块内可以任意重排，因此每个块上热度多重集必须等于目标多重集。
    """
    m = len(p)
    parent = list(range(m))
    rank = [0] * m
    # 每个根上记录该连通块的最小热度，用来判断以后谁还能并进来
    min_h = h[:]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x, y = find(x), find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            x, y = y, x
        parent[y] = x
        min_h[x] = min(min_h[x], min_h[y])
        if rank[x] == rank[y]:
            rank[x] += 1

    # 质量升序，质量相同则热度升序，保证后点只向「左下方」连边
    order = sorted(range(m), key=lambda i: (p[i], h[i]))
    heap = []
    for i in order:
        # 堆里是已处理块的 (最小热度, 根)。最小热度不超过 h[i] 的块都能和当前点合并
        while heap and heap[0][0] <= h[i]:
            tb, x = heappop(heap)
            x = find(x)
            if min_h[x] != tb:
                continue
            union(i, x)
        r = find(i)
        heappush(heap, (min_h[r], r))

    have = defaultdict(list)
    need = defaultdict(list)
    for i in range(m):
        r = find(i)
        have[r].append(h[i])
        need[r].append(t[i])
    for r in have:
        have[r].sort()
        need[r].sort()
        if have[r] != need[r]:
            return False
    return True


def main():
    q = int(input())
    out = []
    for _ in range(q):
        m = int(input())
        raw = list(map(int, input().split()))
        p = raw[0::2]
        h = raw[1::2]
        t = list(map(int, input().split()))
        out.append("YES" if can_match(p, h, t) else "NO")
    print("\n".join(out))


if __name__ == "__main__":
    main()
