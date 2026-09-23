import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
xs = [float(next(it)) for _ in range(n)]
sig, der = Solution().stableSigmoid(xs)
print(" ".join(f"{v:.2f}" for v in sig))
print(" ".join(f"{v:.2f}" for v in der))
