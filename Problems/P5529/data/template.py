import sys

data = sys.stdin.read().strip().split()
it = iter(data)
n = int(next(it))
y = []
pred = []
for _ in range(n):
    y.append(int(next(it)))
    pred.append(float(next(it)))
ans = Solution().binaryAUC(y, pred)
print(f"{ans:.4f}")
