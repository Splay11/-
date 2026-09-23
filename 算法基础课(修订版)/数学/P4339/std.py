import sys
MOD = 10**9 + 7
INV2 = 500000004  # 2 的逆元

def sum_cubes(m: int) -> int:
    # S(m) = (m(m+1)/2)^2  (mod MOD)
    if m <= 0:
        return 0
    m %= MOD
    t = m * ((m + 1) % MOD) % MOD   # m(m+1)
    t = t * INV2 % MOD              # /2
    return t * t % MOD              # 平方

def solve():
    data = sys.stdin.read().strip().split()
    if not data: return
    n = int(data[0])
    ans = 0
    L = 1
    while L <= n:
        q = n // L                  # 当前商
        R = n // q                  # 该商的最右端
        part = (sum_cubes(R) - sum_cubes(L - 1)) % MOD  # 区间立方和
        ans = (ans + part * (q % MOD)) % MOD            # 加权累加
        L = R + 1
    print(ans % MOD)

if __name__ == "__main__":
    solve()
