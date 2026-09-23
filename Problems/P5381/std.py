MOD = 1000000007


def phase_contrib(n, v):
    # 边界：n=1 时下面的倍数循环不会进入，H(1)=0，符合 0 mod 1 = 0
    # 后缀和 suf[i] = v[i]+v[i+1]+...+v[n-1]（已对 MOD 取模）
    # 因为 floor(i/d) 等于 [1,i] 里 d 的倍数个数，
    # 所以 sum_i floor(i/d)*v[i] = sum_{m>=1, m*d<n} suf[m*d]
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = (suf[i + 1] + v[i]) % MOD
    # S = sum_i i*v[i]
    # 余数恒等式：i mod d = i - d*floor(i/d)
    # 因此 H(d) = S - d * sum floor(i/d)*v[i]
    S = 0
    for i in range(n):
        S = (S + i * v[i]) % MOD
    ans = [0] * n
    for d in range(1, n + 1):
        g = 0
        md = d
        # 按调和级数枚举倍数，总复杂度 O(n log n)
        while md < n:
            g += suf[md]
            if g >= MOD:
                g -= MOD
            md += d
        # Python 的 % 对负数会自动加回模数
        ans[d - 1] = (S - d * g) % MOD
    return ans


def main():
    # 单组：第一行长度，第二行 n 个亮度
    n = int(input())
    v = list(map(int, input().split()))
    ans = phase_contrib(n, v)
    # 一行输出 H(1)..H(n)
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
