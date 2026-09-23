# 乘法和开方后的最小值


def factorize(n: int):
    """返回 (质数积, 指数列表)。"""
    primes_prod = 1
    exps = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            primes_prod *= d
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            exps.append(cnt)
        d += 1
    if n > 1:
        primes_prod *= n
        exps.append(1)
    return primes_prod, exps


def solve(n: int):
    if n == 1:
        return 1, 0
    mn, exps = factorize(n)
    max_e = max(exps)
    # 找到 >= max_e 的最小 2 的幂，k 为其对数（开方次数下界）
    pw = 1
    k = 0
    while pw < max_e:
        pw *= 2
        k += 1
    # 一次乘法即可把所有指数补齐到 pw，再开方 k 次得到方根核
    need_mul = any(e != pw for e in exps)
    ops = k + (1 if need_mul else 0)
    return mn, ops


def main():
    n = int(input())
    a, b = solve(n)
    print(a, b)


if __name__ == "__main__":
    main()
