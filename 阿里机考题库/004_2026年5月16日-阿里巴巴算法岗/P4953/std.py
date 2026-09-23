MOD = 10**9 + 7
MAXN = 200000 + 5
# 预处理 2^k，供插空计数使用
pw2 = [1] * MAXN
for i in range(1, MAXN):
    pw2[i] = pw2[i - 1] * 2 % MOD

q = int(input())
for _ in range(q):
    m = int(input())
    z = input().strip()
    kind = len(set(z))
    diff = sum(1 for i in range(m - 1) if z[i] != z[i + 1])
    # 未出现字母均可作失灵键；每种贡献 2^(diff+2)
    print((26 - kind) * pw2[diff + 2] % MOD)
