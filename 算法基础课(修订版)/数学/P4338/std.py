MOD = 998244353

# 快速幂：计算 a^b % MOD
def qpow(a, b):
    res = 1
    a %= MOD
    while b > 0:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

# 计算长度为 n 的所有数字的洞数总和
def solve(n):
    # 特判：n=1 时，0 也算一个一位数
    if n == 1:
        return 6
    # n>=2 时使用推导公式
    return qpow(10, n - 2) * ((54 * (n % MOD) - 4) % MOD) % MOD

if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        n = int(input())
        print(solve(n))
