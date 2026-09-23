MAXB = 1000000


def build_spf():
    # 线性筛最小质因子，后面拆指纹用
    spf = list(range(MAXB + 1))
    i = 2
    while i * i <= MAXB:
        if spf[i] == i:
            j = i * i
            while j <= MAXB:
                if spf[j] == j:
                    spf[j] = i
                j += i
        i += 1
    return spf


def count_pairs(vals):
    spf = build_spf()
    cnt1 = 0
    special = 0
    prime_cnt = {}
    square_cnt = {}
    for x in vals:
        if x == 1:
            # 1 只能和 p^3 或 p*q 配对
            cnt1 += 1
            continue
        n = x
        factors = []
        while n > 1:
            p = spf[n]
            c = 0
            while n % p == 0:
                n //= p
                c += 1
            factors.append((p, c))
        if len(factors) == 1:
            p, c = factors[0]
            if c == 1:
                prime_cnt[p] = prime_cnt.get(p, 0) + 1
            elif c == 2:
                square_cnt[p] = square_cnt.get(p, 0) + 1
            elif c == 3:
                special += 1
        elif len(factors) == 2 and factors[0][1] == 1 and factors[1][1] == 1:
            # 两个不同质数之积
            special += 1
    # 1 与「恰好四因子」的数
    ans = cnt1 * special
    total_p = 0
    for p, c in prime_cnt.items():
        total_p += c
        # 同一个质数两次乘起来是平方，因子个数不是 4
        ans -= c * (c - 1) // 2
        # p 与 p^2 乘积是 p^3
        ans += c * square_cnt.get(p, 0)
    # 不同质数两两配对
    ans += total_p * (total_p - 1) // 2
    return ans


def main():
    # 一行：先 m 再跟 m 个指纹
    parts = list(map(int, input().split()))
    m = parts[0]
    vals = parts[1 : 1 + m]
    print(count_pairs(vals))


if __name__ == "__main__":
    main()
