import sys

data = sys.stdin.read().strip().split()
it = iter(data)
a = float(next(it))
x0 = float(next(it))
eta = float(next(it))
T = int(next(it))
rows = Solution().gradientDescentSqrt(a, x0, eta, T)
for x, L in rows:
    print(f"{x:.4f} {L:.4f}")
