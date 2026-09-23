import numpy as np


class Solution:
    def linear(self, X, W, b):
        # Y = X W + b，b 沿 batch 广播
        X = np.asarray(X, dtype=np.float64)
        W = np.asarray(W, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        return X @ W + b


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it)); din = int(next(it)); dout = int(next(it))
    X = [[float(next(it)) for _ in range(din)] for _ in range(N)]
    W = [[float(next(it)) for _ in range(dout)] for _ in range(din)]
    b = [float(next(it)) for _ in range(dout)]
    Y = Solution().linear(X, W, b)
    lines = []
    for row in Y:
        lines.append(" ".join(f"{float(v):.6f}" for v in row))
    sys.stdout.write("\n".join(lines) + "\n")
