import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it)); dm = int(next(it)); dff = int(next(it))
X = [[float(next(it)) for _ in range(dm)] for _ in range(N)]
W1 = [[float(next(it)) for _ in range(dff)] for _ in range(dm)]
b1 = [float(next(it)) for _ in range(dff)]
W2 = [[float(next(it)) for _ in range(dm)] for _ in range(dff)]
b2 = [float(next(it)) for _ in range(dm)]
Y = Solution().ffn(X, W1, b1, W2, b2)
lines = []
for row in np.asarray(Y):
    lines.append(" ".join(f"{float(v):.2f}" for v in row))
sys.stdout.write("\n".join(lines) + "\n")
