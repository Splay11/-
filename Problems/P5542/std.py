import numpy as np


class Solution:
    def ffn(self, X, W1, b1, W2, b2):
        # FFN(X) = ReLU(X W1 + b1) W2 + b2
        X = np.asarray(X, dtype=np.float64)
        W1 = np.asarray(W1, dtype=np.float64)
        b1 = np.asarray(b1, dtype=np.float64)
        W2 = np.asarray(W2, dtype=np.float64)
        b2 = np.asarray(b2, dtype=np.float64)
        h = X @ W1 + b1
        h = np.maximum(h, 0.0)  # ReLU
        return h @ W2 + b2


if __name__ == "__main__":
    import sys
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
    for row in Y:
        lines.append(" ".join(f"{float(v):.2f}" for v in row))
    sys.stdout.write("\n".join(lines) + "\n")
