import sys

data = sys.stdin.read().strip().split()
it = iter(data)
Lq = int(next(it)); Lkv = int(next(it)); d = int(next(it))
Xq = [[float(next(it)) for _ in range(d)] for _ in range(Lq)]
Xkv = [[float(next(it)) for _ in range(d)] for _ in range(Lkv)]
Wq = [[float(next(it)) for _ in range(d)] for _ in range(d)]
Wk = [[float(next(it)) for _ in range(d)] for _ in range(d)]
Wv = [[float(next(it)) for _ in range(d)] for _ in range(d)]
out = Solution().crossAttention(Xq, Xkv, Wq, Wk, Wv)
lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
sys.stdout.write("\n".join(lines) + "\n")
