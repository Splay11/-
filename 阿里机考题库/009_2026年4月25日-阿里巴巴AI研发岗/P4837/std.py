def count_distinct_masks(feat):
    # feat_i <= 1023，只需枚举 0..1023
    MAX_MASK = 1023
    SIZE = 1024

    # g[mask]：所有包含 mask 的超集特征值的按位与结果
    g = [MAX_MASK] * SIZE

    # exist[mask]：是否存在原初值恰好为 mask
    exist = [False] * SIZE

    for x in feat:
        g[x] = x
        exist[x] = True

    # 超集 DP：合并更大掩码的按位与信息
    for bit in range(10):
        for mask in range(SIZE):
            if (mask & (1 << bit)) == 0:
                super_mask = mask | (1 << bit)
                if exist[super_mask]:
                    g[mask] &= g[super_mask]
                    exist[mask] = True

    ans = 0
    for mask in range(SIZE):
        # 可达当且仅当存在超集且其按位与恰好为 mask
        if exist[mask] and g[mask] == mask:
            ans += 1

    return ans


def main():
    tc = int(input())
    for _ in range(tc):
        m = int(input())
        feat = list(map(int, input().split()))
        print(count_distinct_masks(feat))


if __name__ == "__main__":
    main()
