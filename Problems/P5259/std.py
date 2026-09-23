MOD = 1000000007
MAXA = 100000

phi = list(range(MAXA + 1))
vis = [False] * (MAXA + 1)
for i in range(2, MAXA + 1):
    if not vis[i]:
        for j in range(i, MAXA + 1, i):
            vis[j] = True
            phi[j] = phi[j] // i * (i - 1)


def divisors(d):
    out = []
    t = 1
    while t * t <= d:
        if d % t == 0:
            out.append(t)
            if t * t != d:
                out.append(d // t)
        t += 1
    return out


def prefix(n, d):
    if n <= 0:
        return 0
    s = 0
    for x in divisors(d):
        s = (s + phi[x] * (n // x)) % MOD
    return s


def solve(x, y, left, right):
    d = abs(y - x)
    if d == 0:
        cnt = right - left + 1
        return cnt % MOD * ((2 * x + left + right) % MOD) % MOD * pow(2, MOD - 2, MOD) % MOD
    lo = x + left
    hi = x + right
    return (prefix(hi, d) - prefix(lo - 1, d)) % MOD


if __name__ == "__main__":
    k = int(input())
    for _ in range(k):
        x, y, left, right = map(int, input().split())
        print(solve(x, y, left, right))
