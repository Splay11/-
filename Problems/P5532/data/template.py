import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
max_iter = int(next(it))
alpha = float(next(it))
tol = float(next(it))
X = []
y = []
for _ in range(n):
    X.append([float(next(it)), float(next(it)), float(next(it))])
    y.append(float(next(it)))
m = int(next(it))
X_test = []
for _ in range(m):
    X_test.append([float(next(it)), float(next(it)), float(next(it))])
ans = Solution().logisticRegression(X, y, max_iter, alpha, tol, X_test)
for label, prob in ans:
    print(f"{label} {prob:.4f}")
