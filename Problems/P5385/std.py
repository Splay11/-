# 胜负矩阵里 1 表示后手能赢；最大匹配次数即为必胜场数，得分 = 2*匹配 - m


def max_matching(g):
    m = len(g)
    # 右侧对手艇当前匹配到的我方下标，-1 表示尚未匹配
    match_r = [-1] * m

    def dfs(u, seen):
        # 从我方 u 出发找增广路
        for v in range(m):
            if g[u][v] == 1 and not seen[v]:
                seen[v] = True
                if match_r[v] == -1 or dfs(match_r[v], seen):
                    match_r[v] = u
                    return True
        return False

    cnt = 0
    for u in range(m):
        seen = [False] * m
        if dfs(u, seen):
            cnt += 1
    return cnt


def best_score(g):
    m = len(g)
    return 2 * max_matching(g) - m


def main():
    q = int(input())
    for _ in range(q):
        m = int(input())
        g = []
        for _ in range(m):
            g.append(list(map(int, input().split())))
        print(best_score(g))


if __name__ == "__main__":
    main()
