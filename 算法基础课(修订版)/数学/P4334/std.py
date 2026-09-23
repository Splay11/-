import sys
import math

def divisors_leq(v, n):
    # 返回 v 的所有不超过 n 的因子
    res = []
    i = 1
    while i * i <= v:
        if v % i == 0:
            if i <= n:
                res.append(i)
            j = v // i
            if j != i and j <= n:
                res.append(j)
        i += 1
    return res

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n, x, y = map(int, data)

    # |A ∪ B|
    g = math.gcd(x, y)
    lcm_xy = (x // g) * y  # Python 整数无溢出
    M = n // x + n // y - (n // lcm_xy)

    # 不超过 n 的因子集合（去重）
    S = set(divisors_leq(x, n)) | set(divisors_leq(y, n))

    # 统计额外补计的因子
    extra = sum(1 for d in S if d % x != 0 and d % y != 0)

    print(M + extra)

if __name__ == "__main__":
    solve()
