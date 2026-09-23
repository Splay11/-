import math
import random

# 64 位确定性 Miller-Rabin 的一组底
MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def is_prime(n):
    if n < 2:
        return False
    # 先筛掉很小的素因子
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in MR_BASES:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        ok = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                ok = True
                break
        if not ok:
            return False
    return True


def pollard(n):
    # 找出 n 的一个真因子；偶因子单独处理
    if n % 2 == 0:
        return 2
    if is_prime(n):
        return n
    while True:
        x = random.randrange(2, n)
        y = x
        c = random.randrange(1, n)
        d = 1
        while d == 1:
            x = (pow(x, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def min_prime_factor(n):
    # n>=2 的最小素因子
    if n % 2 == 0:
        return 2
    if is_prime(n):
        return n
    f = pollard(n)
    return min(min_prime_factor(f), min_prime_factor(n // f))


def smallest_odd_prime_factor(n):
    # 先剥掉全部因子 2；若只剩 1，说明 n 是 2 的幂
    while n % 2 == 0:
        n //= 2
    if n == 1:
        return -1
    # 剩下的奇数的最小素因子，就是原数的最小奇素因子
    return min_prime_factor(n)


def main():
    random.seed(1)
    q = int(input())
    for _ in range(q):
        x = int(input())
        print(smallest_odd_prime_factor(x))


if __name__ == "__main__":
    main()
