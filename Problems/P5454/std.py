# 枚举每个探测原点，按平方距离分桶，同一桶内 c 个点贡献 c*(c-1) 组有序对


def count_equidistant(loc):
    """
    loc[p] = (u_p, v_p)。统计有序三元 (p, q, r) 的个数：
    p 到 q 的欧氏距离等于 p 到 r 的欧氏距离，且 q、r、p 两两不同。
    比较平方距离，避免开方带来的浮点误差。
    """
    m = len(loc)
    ans = 0
    # 每个点都当一次探测原点
    for p in range(m):
        ux, uy = loc[p]
        buckets = {}
        for q in range(m):
            if p == q:
                continue
            dx = loc[q][0] - ux
            dy = loc[q][1] - uy
            # 平方距离；Python 整数任意长，坐标到 1e5 也不会溢出
            d2 = dx * dx + dy * dy
            buckets[d2] = buckets.get(d2, 0) + 1
        # 同一距离有 c 个点：从中挑有序对 (q, r) 共 c*(c-1) 种
        for c in buckets.values():
            ans += c * (c - 1)
    return ans


def main():
    m = int(input())
    loc = []
    for _ in range(m):
        u, v = map(int, input().split())
        loc.append((u, v))
    print(count_equidistant(loc))


if __name__ == "__main__":
    main()
