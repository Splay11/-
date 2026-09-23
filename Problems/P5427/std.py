# 从下标 0 按当前值的质因数左右跳，判断能否到达最后一个下标
#
# 把每个下标看成图上的点。seq[p] 的每个质因数 d 连向 p+d、p-d（不越界）。
# 从 0 做 BFS，到达 m-1 即成功。长度为 1 时已经在终点。


def prime_factors(x):
    """分解 x 的全部不同质因数。1 没有质因数。"""
    if x <= 1:
        return []
    factors = []
    # 先剥 2
    if x % 2 == 0:
        factors.append(2)
        while x % 2 == 0:
            x //= 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 2
    # 剩下大于 1 的就是最后一个质数
    if x > 1:
        factors.append(x)
    return factors


def can_reach(seq):
    """从下标 0 出发，按质因数左右跳，能否到达最后一个下标。"""
    m = len(seq)
    # 只有一个位置时，起点就是终点
    if m == 1:
        return True
    vis = [False] * m
    q = [0]
    vis[0] = True
    head = 0
    while head < len(q):
        p = q[head]
        head += 1
        # 枚举当前值的每个质因数，尝试左右跳
        for d in prime_factors(seq[p]):
            for nxt in (p + d, p - d):
                if 0 <= nxt < m and not vis[nxt]:
                    if nxt == m - 1:
                        return True
                    vis[nxt] = True
                    q.append(nxt)
    return False


def main():
    # 一行空格分隔的整个序列
    seq = list(map(int, input().split()))
    print("true" if can_reach(seq) else "false")


if __name__ == "__main__":
    main()
