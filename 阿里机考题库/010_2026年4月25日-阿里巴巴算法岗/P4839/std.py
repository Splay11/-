MOD = 10**9 + 7

T = int(input())
lens = []
tokens = []
max_l = 0

# 读入每组目标编码长度与 token（评测按原题 I/O）
for _ in range(T):
    L = int(input())
    token = input().strip()
    lens.append(L)
    tokens.append(token)
    max_l = max(max_l, L)

# 预处理阶乘：L 次任意位置插入的序列数恒为 L!
fact = [1] * (max_l + 1)
for i in range(1, max_l + 1):
    fact[i] = fact[i - 1] * i % MOD

for L in lens:
    print(fact[L])
