import sys

data = sys.stdin.read().strip().split()
it = iter(data)
m = int(next(it))
n = int(next(it))
P = [[float(next(it)) for _ in range(n)] for _ in range(m)]
Q = [[float(next(it)) for _ in range(n)] for _ in range(m)]
ans = Solution().averageKLDivergence(P, Q)
print(f"{ans:.6f}")
