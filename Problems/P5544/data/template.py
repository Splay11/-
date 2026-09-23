import sys
import numpy as np

data = sys.stdin.read().strip().split()
it = iter(data)
L = int(next(it)); K = int(next(it)); S = int(next(it)); P = int(next(it))
x = [float(next(it)) for _ in range(L)]
w = [float(next(it)) for _ in range(K)]
C, y = Solution().im2col_conv1d(x, w, S, P)
C = np.asarray(C)
y = np.asarray(y)
O = C.shape[0]
lines = [f"{O} {K}"]
for row in C:
    lines.append(" ".join(f"{float(v):.4f}" for v in row))
lines.append(" ".join(f"{float(v):.4f}" for v in y))
sys.stdout.write("\n".join(lines) + "\n")
