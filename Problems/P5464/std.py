NEG = -10**30


def max_gain(v):
    # 三段 DP：尚未加速 / 正在加速 / 加速已结束
    # d0：当前结尾且整段没加速；d1：当前项在窗口内；d2：窗口已结束
    d0 = v[0]
    d1 = 2 * v[0]
    d2 = NEG
    ans = d0 if d0 > d1 else d1
    for i in range(1, len(v)):
        x = v[i]
        # 不加速：新开一段或接到旧段后面
        nd0 = x if x > d0 + x else d0 + x
        t = 2 * x
        # 正在加速：只取当前、从未加速转入、或继续加倍
        nd1 = t
        if d0 + t > nd1:
            nd1 = d0 + t
        if d1 + t > nd1:
            nd1 = d1 + t
        # 加速已结束：只能加原收益
        nd2 = d1 + x
        if d2 + x > nd2:
            nd2 = d2 + x
        d0, d1, d2 = nd0, nd1, nd2
        if d0 > ans:
            ans = d0
        if d1 > ans:
            ans = d1
        if d2 > ans:
            ans = d2
    return ans


def solve_all(groups):
    return [max_gain(v) for v in groups]


def main():
    # 第一行组数；每行先 m 再跟 m 个收益
    k = int(input())
    groups = []
    for _ in range(k):
        parts = list(map(int, input().split()))
        m = parts[0]
        v = parts[1:]
        groups.append(v[:m])
    # 一行输出 k 个答案，空格隔开
    ans = solve_all(groups)
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
