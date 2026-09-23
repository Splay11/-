import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
d_in = int(next(it))
d_h = int(next(it))
eta = float(next(it))
y = [float(next(it)) for _ in range(n)]
X = [[float(next(it)) for _ in range(d_in)] for _ in range(n)]
W1 = [[float(next(it)) for _ in range(d_h)] for _ in range(d_in)]
W2 = [[float(next(it))] for _ in range(d_h)]
yhat, loss, W1n, W2n = Solution().trainTwoLayerMLP(X, y, W1, W2, eta)
print(" ".join(f"{v:.4f}" for v in yhat))
print(f"{loss:.4f}")
for row in W1n:
    print(" ".join(f"{v:.4f}" for v in row))
for v in W2n:
    print(f"{v:.4f}")
