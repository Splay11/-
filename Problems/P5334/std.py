# 层台栈道巡回：无向图欧拉回路（Hierholzer）
# 第 r 层第 c 个台位编号为 r*(r-1)/2+c；每层与上一层拼出若干三角形，三条边都要走恰好一次


def solve(h, start):
    # 台位总数：第 1..h 层分别有 1..h 个点
    n = h * (h + 1) // 2
    g = [[] for _ in range(n + 1)]
    eu = []
    ev = []

    def add(a, b):
        # 无向边存一次，两端邻接表都记下边号，方便删除（标记）
        eid = len(eu)
        eu.append(a)
        ev.append(b)
        g[a].append(eid)
        g[b].append(eid)

    for r in range(2, h + 1):
        # base：本层第一个台位的编号减 1；prev：上一层第一个台位的编号减 1
        base = r * (r - 1) // 2
        prev = (r - 1) * (r - 2) // 2
        for c in range(1, r):
            u = base + c
            v = base + c + 1
            w = prev + c
            # 同层相邻栈道，以及连接到上一层同一个台位的两条斜栈道，构成一个小三角
            add(u, v)
            add(u, w)
            add(v, w)

    used = [False] * len(eu)
    ptr = [0] * (n + 1)
    stack = [start]
    circ = []
    # Hierholzer：一直沿未用边走，走不了时把当前点弹入回路（得到的是逆序）
    while stack:
        u = stack[-1]
        while ptr[u] < len(g[u]) and used[g[u][ptr[u]]]:
            ptr[u] += 1
        if ptr[u] == len(g[u]):
            circ.append(u)
            stack.pop()
        else:
            eid = g[u][ptr[u]]
            ptr[u] += 1
            used[eid] = True
            a = eu[eid]
            b = ev[eid]
            stack.append(b if a == u else a)
    circ.reverse()
    return circ


def main():
    k = int(input())
    for _ in range(k):
        h, s = map(int, input().split())
        path = solve(h, s)
        print(" ".join(str(x) for x in path))


if __name__ == "__main__":
    main()
