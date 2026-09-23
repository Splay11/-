import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it)); din = int(next(it)); dout = int(next(it))
X = [[float(next(it)) for _ in range(din)] for _ in range(N)]
W = [[float(next(it)) for _ in range(dout)] for _ in range(din)]
b = [float(next(it)) for _ in range(dout)]
Y = Solution().linear(X, W, b)
lines = []
for row in np.asarray(Y):
    lines.append(" ".join(f"{float(v):.6f}" for v in row))
sys.stdout.write("\n".join(lines) + "\n")
