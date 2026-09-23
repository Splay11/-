from collections import deque


def min_waves(p, rel):
    """
    最少波次 = DAG 上最长链包含的模型个数。
    rel 中 (u, v) 表示 v 必须等 u 先结束，建边 u -> v。
    """
    graph = [[] for _ in range(p + 1)]
    indeg = [0] * (p + 1)
    for u, v in rel:
        graph[u].append(v)
        indeg[v] += 1

    # dp[x]：以 x 结尾的最长链长度；孤立点为 1
    dp = [1] * (p + 1)
    q = deque()
    for i in range(1, p + 1):
        if indeg[i] == 0:
            q.append(i)

    while q:
        u = q.popleft()
        for v in graph[u]:
            # 先走完 u 再走 v，链长至少是 dp[u] + 1
            if dp[u] + 1 > dp[v]:
                dp[v] = dp[u] + 1
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    ans = 1
    for i in range(1, p + 1):
        if dp[i] > ans:
            ans = dp[i]
    return ans


def main():
    p, e = map(int, input().split())
    rel = []
    for _ in range(e):
        u, v = map(int, input().split())
        rel.append((u, v))
    print(min_waves(p, rel))


if __name__ == "__main__":
    main()
