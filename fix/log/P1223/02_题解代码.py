import math, sys
def solve(n):
    if n % 2 == 1:
        return n // 2, n - n // 2
    a = n // 2
    while math.gcd(a, n) != 1:
        a -= 1
    return a, n - a
data = list(map(int, sys.stdin.read().split()))
t = data[0]
out = []
for n in data[1:1+t]:
    a, b = solve(n)
    out.append(f"{a} {b}")
print("\n".join(out))
