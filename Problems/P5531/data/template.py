import sys

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it))
xs = []
ys = []
for _ in range(N):
    xs.append(float(next(it)))
    ys.append(float(next(it)))
degree = int(next(it))
coef = Solution().polynomialRegression(xs, ys, degree)

def fmt(c):
    s = f"{c:.4f}"
    if s.endswith("00"):
        return s[:-2]
    return s

print(" ".join(fmt(c) for c in coef))
