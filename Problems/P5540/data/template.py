import sys

data = sys.stdin.read().strip().split()
it = iter(data)
d_in = int(next(it))
d_h = int(next(it))
d_out = int(next(it))
x = [float(next(it)) for _ in range(d_in)]
W1 = [[float(next(it)) for _ in range(d_h)] for _ in range(d_in)]
b1 = [float(next(it)) for _ in range(d_h)]
W2 = [[float(next(it)) for _ in range(d_out)] for _ in range(d_h)]
b2 = [float(next(it)) for _ in range(d_out)]
y = [float(next(it)) for _ in range(d_out)]
yhat, loss, dW1, db1, dW2, db2 = Solution().twoLayerFCForwardBackward(
    x, W1, b1, W2, b2, y
)
print(" ".join(f"{v:.4f}" for v in yhat))
print(f"{loss:.4f}")
for row in dW1:
    print(" ".join(f"{v:.4f}" for v in row))
print(" ".join(f"{v:.4f}" for v in db1))
for row in dW2:
    print(" ".join(f"{v:.4f}" for v in row))
print(" ".join(f"{v:.4f}" for v in db2))
