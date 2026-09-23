import sys

def read_mat(it, rows, cols):
    return [[float(next(it)) for _ in range(cols)] for _ in range(rows)]

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it)); d = int(next(it)); n_h = int(next(it)); n_q = int(next(it))
d_c = int(next(it)); d_h = int(next(it)); d_rope = int(next(it))
X = read_mat(it, N, d)
W_DQ = read_mat(it, d, n_q)
W_UQ = read_mat(it, n_q, n_h * d_h)
W_DKV = read_mat(it, d, d_c)
W_UK = read_mat(it, d_c, n_h * d_h)
W_UV = read_mat(it, d_c, n_h * d_h)
W_QR = read_mat(it, d, n_h * d_rope)
W_KR = read_mat(it, d, d_rope)
W_o = read_mat(it, n_h * d_h, d)
out = Solution().mlaForward(X, W_DQ, W_UQ, W_DKV, W_UK, W_UV, W_QR, W_KR, W_o, n_h, d_h, d_rope)
for row in out:
    print(" ".join(f"{x:.4f}" for x in row))
