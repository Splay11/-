import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it)); d = int(next(it))
X = [[float(next(it)) for _ in range(d)] for _ in range(N)]
gamma = [float(next(it)) for _ in range(d)]
beta = [float(next(it)) for _ in range(d)]
eps = float(next(it))
mu, var, Y = Solution().batch_norm(X, gamma, beta, eps)
lines = []
lines.append(" ".join(f"{float(v):.2f}" for v in np.asarray(mu)))
lines.append(" ".join(f"{float(v):.2f}" for v in np.asarray(var)))
for row in np.asarray(Y):
    lines.append(" ".join(f"{float(v):.2f}" for v in row))
sys.stdout.write("\n".join(lines) + "\n")
