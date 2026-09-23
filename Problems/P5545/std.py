import numpy as np


class Solution:
    def max_pool2d(self, X, k, s):
        # X: (C,H,W)，逐通道取窗口最大值
        X = np.asarray(X, dtype=np.float64)
        C, H, W = X.shape
        Hout = (H - k) // s + 1
        Wout = (W - k) // s + 1
        Y = np.zeros((C, Hout, Wout), dtype=np.float64)
        for c in range(C):
            for i in range(Hout):
                for j in range(Wout):
                    # 窗口 [si:si+k, sj:sj+k] 取 max
                    patch = X[c, i * s : i * s + k, j * s : j * s + k]
                    Y[c, i, j] = np.max(patch)
        return Y


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    C = int(next(it)); H = int(next(it)); W = int(next(it)); k = int(next(it)); s = int(next(it))
    X = [[[0.0] * W for _ in range(H)] for _ in range(C)]
    for c in range(C):
        for h in range(H):
            for w in range(W):
                X[c][h][w] = float(next(it))
    Y = Solution().max_pool2d(X, k, s)
    blocks = []
    for c in range(Y.shape[0]):
        rows = [" ".join(f"{float(v):.2f}" for v in row) for row in Y[c]]
        blocks.append("\n".join(rows))
    sys.stdout.write("\n".join(blocks) + "\n")
