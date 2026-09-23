import sys

def read_mat(it, rows, cols):
    return [[float(next(it)) for _ in range(cols)] for _ in range(rows)]

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it)); d_in = int(next(it)); d_out = int(next(it)); r = int(next(it))
alpha = float(next(it))
X = read_mat(it, n, d_in)
W = read_mat(it, d_in, d_out)
A = read_mat(it, d_in, r)
B = read_mat(it, r, d_out)
out = Solution().loraForward(X, W, A, B, alpha)
for row in out:
    print(" ".join(f"{x:.4f}" for x in row))
