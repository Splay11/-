import sys

data = sys.stdin.read().strip().split()
it = iter(data)
L = int(next(it)); d = int(next(it)); h = int(next(it))
X = [[float(next(it)) for _ in range(d)] for _ in range(L)]
Wq = [[float(next(it)) for _ in range(d)] for _ in range(d)]
Wk = [[float(next(it)) for _ in range(d)] for _ in range(d)]
Wv = [[float(next(it)) for _ in range(d)] for _ in range(d)]
Wo = [[float(next(it)) for _ in range(d)] for _ in range(d)]
out = Solution().multiHeadAttention(X, Wq, Wk, Wv, Wo, h)
lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
sys.stdout.write("\n".join(lines) + "\n")
