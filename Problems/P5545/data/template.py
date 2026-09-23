import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
C = int(next(it)); H = int(next(it)); W = int(next(it)); k = int(next(it)); s = int(next(it))
X = [[[0.0] * W for _ in range(H)] for _ in range(C)]
for c in range(C):
    for h in range(H):
        for w in range(W):
            X[c][h][w] = float(next(it))
Y = np.asarray(Solution().max_pool2d(X, k, s))
blocks = []
for c in range(Y.shape[0]):
    rows = [" ".join(f"{float(v):.2f}" for v in row) for row in Y[c]]
    blocks.append("\n".join(rows))
sys.stdout.write("\n".join(blocks) + "\n")
