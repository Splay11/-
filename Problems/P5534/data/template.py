import sys

data = sys.stdin.read().strip().split()
it = iter(data)
N = int(next(it))
y = [int(next(it)) for _ in range(N)]
p = [float(next(it)) for _ in range(N)]
ans = Solution().binaryCrossEntropy(y, p)
print(f"{ans:.2f}")
