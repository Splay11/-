def sieve(n):
    vis = [True] * (n + 1)
    ps = []
    for i in range(2, n + 1):
        if not vis[i]:
            continue
        ps.append(i)
        start = i * i
        if start > n:
            continue
        for j in range(start, n + 1, i):
            vis[j] = False
    return ps

primes = sieve(32000)

def factorize(x):
    fac = []
    for p in primes:
        if p * p > x:
            break
        if x % p == 0:
            fac.append(p)
            while x % p == 0:
                x //= p
    if x > 1:
        fac.append(x)
    return fac

m, t = map(int, input().split())
v = list(map(int, input().split()))  # 传感读数
pid, pc = {}, 0
fac_ids = [[] for _ in range(m)]
for i, x in enumerate(v):
    if x == 1:
        continue
    for p in factorize(x):
        if p not in pid:
            pid[p] = pc
            pc += 1
        fac_ids[i].append(pid[p])

vals = sorted(set(v))

def check(M):
    if t == 1:
        return any(x <= M for x in v)
    best = [0] * pc
    mx = 0
    for i, x in enumerate(v):
        if x > M or x == 1:
            continue
        dp = 1
        for j in fac_ids[i]:
            if best[j] + 1 > dp:
                dp = best[j] + 1
        if dp > mx:
            mx = dp
        if mx >= t:
            return True
        for j in fac_ids[i]:
            if best[j] < dp:
                best[j] = dp
    return False

lo, hi = 0, len(vals) - 1
res = -1
while lo <= hi:
    mid = (lo + hi) // 2
    if check(vals[mid]):
        res = vals[mid]
        hi = mid - 1
    else:
        lo = mid + 1
print(res)
