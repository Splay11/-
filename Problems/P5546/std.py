import numpy as np


class Solution:
    def batch_norm(self, X, gamma, beta, eps):
        # 训练模式：用当前 batch 的均值/方差（总体方差 1/N）
        X = np.asarray(X, dtype=np.float64)
        gamma = np.asarray(gamma, dtype=np.float64)
        beta = np.asarray(beta, dtype=np.float64)
        mu = X.mean(axis=0)
        var = X.var(axis=0)  # ddof=0，即 1/N
        xhat = (X - mu) / np.sqrt(var + eps)
        Y = gamma * xhat + beta
        return mu, var, Y


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it)); d = int(next(it))
    X = [[float(next(it)) for _ in range(d)] for _ in range(N)]
    gamma = [float(next(it)) for _ in range(d)]
    beta = [float(next(it)) for _ in range(d)]
    eps = float(next(it))
    mu, var, Y = Solution().batch_norm(X, gamma, beta, eps)
    lines = []
    lines.append(" ".join(f"{float(v):.2f}" for v in mu))
    lines.append(" ".join(f"{float(v):.2f}" for v in var))
    for row in Y:
        lines.append(" ".join(f"{float(v):.2f}" for v in row))
    sys.stdout.write("\n".join(lines) + "\n")
