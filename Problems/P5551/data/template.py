import sys

data = sys.stdin.read().strip().split()
it = iter(data)
L = int(next(it)); d = int(next(it)); h = int(next(it)); dff = int(next(it))

def read_mat(r, c):
    return [[float(next(it)) for _ in range(c)] for _ in range(r)]

X = read_mat(L, d)
Wq = read_mat(d, d)
Wk = read_mat(d, d)
Wv = read_mat(d, d)
Wo = read_mat(d, d)
W1 = read_mat(d, dff)
b1 = [float(next(it)) for _ in range(dff)]
W2 = read_mat(dff, d)
b2 = [float(next(it)) for _ in range(d)]
out = Solution().transformerEncoderBlock(X, Wq, Wk, Wv, Wo, W1, b1, W2, b2, h)
lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
sys.stdout.write("\n".join(lines) + "\n")
