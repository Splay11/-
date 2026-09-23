import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it)); d = int(next(it)); tau = float(next(it))
A = [[float(next(it)) for _ in range(d)] for _ in range(n)]
P = [[float(next(it)) for _ in range(d)] for _ in range(n)]
print(f"{Solution().infoNCE(A, P, tau):.4f}")
