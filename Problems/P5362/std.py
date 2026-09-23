import bisect


def min_swaps(d):
    # 环上把 0 挪到偶数位或奇数位；0 之间不能交叉，只差一个循环错位
    m = len(d) // 2
    # 所有 0 的下标，已按环上顺时针排好
    pos = []
    for i in range(len(d)):
        if d[i] == "0":
            pos.append(i)
    ans = 10**18
    for start in (0, 1):
        # start=0：目标是 0101...；start=1：目标是 1010...
        # b[i] 记录「第 i 个 0 相对第 i 个目标格」的有向偏移
        b = []
        for i in range(m):
            b.append(pos[i] - 2 * i - start)
        # min_k sum |b[i] + 2k|，k 取 -(m-1)..(m-1)，覆盖顺时针/逆时针错位
        # 改写成 sum |x - a[i]|，x = 2k
        a = sorted(-x for x in b)
        pref = [0]
        for v in a:
            pref.append(pref[-1] + v)

        def l1(x):
            # 有序点集 a 到点 x 的曼哈顿和
            left = bisect.bisect_right(a, x)
            return x * left - pref[left] + (pref[m] - pref[left]) - x * (m - left)

        for k in range(-(m - 1), m):
            cur = l1(2 * k)
            if cur < ans:
                ans = cur
    return ans


def main():
    # 单组：半长 m，随后一整圈色片
    m = int(input().strip())
    d = input().strip()
    print(min_swaps(d))


if __name__ == "__main__":
    main()
