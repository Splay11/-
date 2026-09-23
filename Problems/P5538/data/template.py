import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
d = int(next(it))
eta = float(next(it))
T = int(float(next(it)))
X, y = [], []
for _ in range(n):
    row = [float(next(it)) for _ in range(d)]
    yi = float(next(it))
    X.append(row)
    y.append(yi)
w, bb = Solution().sgdLinearRegression(X, y, eta, T)
print(" ".join(f"{v:.4f}" for v in w))
print(f"{bb[0]:.4f}")
