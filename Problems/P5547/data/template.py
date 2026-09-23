import sys

data = sys.stdin.read().strip().split()
it = iter(data)
d = int(next(it)); T = int(next(it))
alpha = float(next(it)); beta1 = float(next(it)); beta2 = float(next(it)); eps = float(next(it))
theta = [float(next(it)) for _ in range(d)]
grads = [[float(next(it)) for _ in range(d)] for _ in range(T)]
outs = Solution().adamUpdate(theta, grads, alpha, beta1, beta2, eps)
lines = [" ".join(f"{float(x):.4f}" for x in row) for row in outs]
sys.stdout.write("\n".join(lines) + "\n")
