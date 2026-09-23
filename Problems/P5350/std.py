NEG = -10**18


def max_value(h, w, v):
    # 走了 t 步后：A 在 (t-c1, c1)，B 在 (t-(w-1-c2), c2)
    # 因为 A 只会下/右，横坐标就是向右次数；B 的向左次数是 (w-1-c2)
    end_t = h + w - 2
    dp = [[NEG] * w for _ in range(w)]
    # 起点不同（w>=3），把两个起点的价值都算上
    dp[0][w - 1] = v[0][0] + v[0][w - 1]
    for t in range(end_t):
        ndp = [[NEG] * w for _ in range(w)]
        for c1 in range(w):
            for c2 in range(w):
                cur = dp[c1][c2]
                if cur == NEG:
                    continue
                r1 = t - c1
                r2 = t - (w - 1 - c2)
                if r1 < 0 or r1 >= h or r2 < 0 or r2 >= h:
                    continue
                # A：向下或向右
                moves_a = []
                if r1 + 1 < h:
                    moves_a.append((r1 + 1, c1))
                if c1 + 1 < w:
                    moves_a.append((r1, c1 + 1))
                # B：向下或向左
                moves_b = []
                if r2 + 1 < h:
                    moves_b.append((r2 + 1, c2))
                if c2 - 1 >= 0:
                    moves_b.append((r2, c2 - 1))
                for nr1, nc1 in moves_a:
                    for nr2, nc2 in moves_b:
                        # 同一时刻不能站在同一格
                        if nr1 == nr2 and nc1 == nc2:
                            continue
                        val = cur + v[nr1][nc1] + v[nr2][nc2]
                        if val > ndp[nc1][nc2]:
                            ndp[nc1][nc2] = val
        dp = ndp
    return dp[w - 1][0]


def main():
    parts = input().split()
    h = int(parts[0])
    w = int(parts[1])
    v = []
    for _ in range(h):
        v.append(list(map(int, input().split())))
    print(max_value(h, w, v))


if __name__ == "__main__":
    main()
